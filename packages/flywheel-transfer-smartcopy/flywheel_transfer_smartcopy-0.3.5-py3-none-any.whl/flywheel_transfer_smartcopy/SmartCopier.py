import json
import logging
import sys
import time
from dataclasses import dataclass
from typing import Union

import flywheel
import fw_utils
import requests
from flywheel_transfer_utils import FlywheelUtils
from fw_client import FWClient, NotFound

HIERARCHY = FlywheelUtils.PRIMARY_HIERARCHY
AnyContainer = FlywheelUtils.AnyContainer
CONTAINER_ID_FORMAT = FlywheelUtils.CONTAINER_ID_FORMAT

log = logging.getLogger(__name__)

WAIT_TIMEOUT = 4 * 60 * 60  # Timeout=4hours


@dataclass
class CopyConfig:
    """A dataclass that contains all the configuration options for the copier."""

    exclude_empty: bool = True
    include_rules: list = None
    exclude_rules: list = None
    delete_snapshots: bool = True
    exclude_analysis: bool = False
    exclude_notes: bool = False
    exclude_tags: bool = False


class SmartCopier:
    """This class's responsibility is to create a smartcopy of a project.

    The SmartCopier gets passed the source project and the label of the destination project.  Workflow is:
    1. Initialize a config specifying any filters and options
    2. Initiate a smart copy by providing a source project and final project label.
    3. Wait for it to finish
    4. Delete the smart copy snapshot

    This synchronous operation is good for gears that require a smart copy.

    Attributes
    ----------
    client: flywheel.Client()
    config: configuration settings to be used by the smart copy

    Examples
    --------
    >>> import flywheel
    >>> import os
    >>> api_key = os.environ["LATEST_API"]
    >>> fw = flywheel.Client(os.environ["LATEST_API"])
    >>> source_project = fw.get_project("<source_project_id>")
    >>> dest_project = "<dest_project_label>"
    >>> copy_config = SmartCopier.CopyConfig(exclude_empty=True, additional_filters="file.type=nifti", delete_snapshots=True)
    >>> copier = SmartCopier.SmartCopier(api_key="<my_api_key>", source_project=source_project, destination_project=dest_project, config=copy_config)

    or alternatively:
    >>> import flywheel
    >>> import os
    >>> api_key = os.environ["LATEST_API"]
    >>> copy_config = SmartCopier.CopyConfig(exclude_empty=True, additional_filters="file.type=nifti", delete_snapshots=True)
    >>> copier = SmartCopier.SmartCopier(api_key="<my_api_key>", source_project="<source_project_id>", destination_project="<dest_project_label>", config=copy_config)

    To Copy:
    >>> copier.smart_copy_project()


    """

    def __init__(
        self,
        client: FWClient,
        config: CopyConfig = None,
    ):
        """

        Parameters
        ----------
        client: FWClient
            the flywheel HTTP client
        config: CopyConfig
            A dataclass that contains all the configuration options for the copier
        """
        self.client = client
        self.config = config
        self._source_project = None
        self._destination_project = None
        self._destination_group = None

    def initialize_source_project(
        self, source_project: Union[flywheel.Project, str]
    ) -> None:
        """set the source project value.

        Set the source project to a flywheel project that's passed in,
        or load the project from a string.

        Args:
            source_project (Union[flywheel.Project, str]): a flywheel project or a project identification string

        Raises:
            NotFound: if the project can't be found.
        """

        # If the source project is already a flywheel project, just set it.
        if isinstance(source_project, flywheel.Project):
            self._source_project = source_project
            return

        # if not we have to try to load it.  If we can't find it, raise an error.
        project = self._load_project_str(source_project)
        if project is None:
            raise NotFound("Source project %s not found" % source_project)
        self._source_project = source_project

    def validate_dest_project(self, desired_destination_project: str) -> None:
        """Validates that the destination project does not exist.

        If the user specifies a project label, we assume that the project is in the same group as the source project.
        However we allow the user to override the destination group by providing a lookup string (fw://group/project),
        as long as the target project doesn't exist.

        Args:
            desired_destination_project (str): the destination project label/lookup string to validate.

        Raises:
            ValueError: if the project exists

        """
        # First do a simple check to see if the destination project exists.
        existing_project = self._load_project_str(desired_destination_project)
        if existing_project:
            raise ValueError(
                "Destination project %s already exists" % desired_destination_project
            )

        # Assume that we will use the source project group as the destination group.
        self._destination_group = self._source_project.group

        # If the project identifier is in the flywheel lookup format (fw://group/project),
        # we need to ensure that the target group exists.
        if FlywheelUtils.is_lookup(desired_destination_project):
            parts = FlywheelUtils.breakout_lookup(desired_destination_project)
            group = parts[0]
            desired_destination_project = parts[1]  # Just extract the project name

            try:
                # If we can successfully get the group, we'll allow the user to use it as a destination.
                group = FlywheelUtils.get_container(
                    self.client, id_=group, container_type="group"
                )
            except NotFound:
                # If not just raise an error.  Nothing more to do here.
                raise ValueError(f"Destination group {group} not found")
            # The group exists, so overwrite that as the destination group.
            self._destination_group = group._id

        # set the destination project
        self._destination_project = desired_destination_project

    def create_filters(
        self,
        additional_include_rules: list = None,
        additional_exclude_rules: list = None,
    ) -> tuple[list, list]:
        """Create include and exclude rule lists for the smart copy

        Args:
            additional_include_rules: a list of include filters
            additional_exclude_rules: a list of exclude filters

        Returns:
            include_rules: a list of include rules
            exclude_rules: a list of exclude rules

        """
        include_rules = []
        exclude_rules = []

        if self.config.include_rules:
            include_rules.extend(self.config.include_rules)
        if self.config.exclude_rules:
            exclude_rules.extend(self.config.exclude_rules)

        if additional_include_rules:
            include_rules.append(additional_include_rules)
        if additional_exclude_rules:
            exclude_rules.append(additional_exclude_rules)

        return include_rules, exclude_rules

    def reset_values(self) -> None:
        """Reset the values of the copier"""
        self._source_project = None
        self._destination_project = None
        self._destination_group = None

    def smart_copy_project(
        self,
        source_project: Union[flywheel.Project, str],
        destination_project: str,
        additional_include_filter: Union[str, None] = None,
        additional_exclude_filter: Union[str, None] = None,
    ) -> str:
        """Initiate a smart copy of a project and wait for it to complete.

        Args:
            source_project: The source project to copy.
            destination_project: The name of the destination project to create (can be project label or fw lookup address)
            additional_include_filter: an additional include filter to add to the smart copy
            additional_exclude_filter: an additional exclude filter to add to the smart copy

        Returns:
            the id of the smartcopy project

        """

        self.initialize_source_project(source_project)
        self.validate_dest_project(destination_project)
        include_rules, exclude_rules = self.create_filters(
            additional_include_filter, additional_exclude_filter
        )

        log.info(
            f"Smart copying {self._source_project.label} with filter include: {include_rules}, exclude: {exclude_rules}"
        )
        data = {
            "group_id": self._destination_group,
            "project_label": self._destination_project,
            "filter": {
                "exclude_analysis": self.config.exclude_analysis,
                "exclude_notes": self.config.exclude_notes,
                "exclude_tags": self.config.exclude_tags,
                "include_rules": include_rules,
                "exclude_rules": exclude_rules,
                "exclude_empty_containers": self.config.exclude_empty,
            },
        }

        # Initiate the copy and wait for it to complete
        copy_rsp = self.client.post(
            f"/api/projects/{self._source_project._id}/copy", data=json.dumps(data)
        )
        self.wait_for_copy(copy_rsp)
        if self.config.delete_snapshots:
            self.delete_snapshot(self._source_project._id, copy_rsp["snapshot_id"])

        self.reset_values()

        return copy_rsp["project_id"]

    def is_copy_done(self, project_id: str, snapshot_id: str) -> bool:
        """Returns True if a smartcopy is done, False otherwise."""

        response = self.client.get(
            f"/api/projects/{project_id}/copy/{snapshot_id}/status"
        )
        return True if response["copy_status"] == "completed" else False

    def wait_for_copy(self, copy_rsp: dict) -> None:
        """Wait for a smartcopy to complete

        Args:
            copy_rsp: the response generated when a smart copy is initialized

        """
        # wait for all copies to complete
        log.debug("Waiting for copy to complete")
        start_time = time.time()
        while True:
            if self.is_copy_done(copy_rsp["project_id"], copy_rsp["snapshot_id"]):
                log.info(f"Copy project {copy_rsp['project_id']} complete")
                break
            if time.time() - start_time > WAIT_TIMEOUT:
                log.error(
                    "Wait timeout for copy of project %s with snapshot %s"
                    % (copy_rsp["project_id"], copy_rsp["snapshot_id"])
                )
                sys.exit(-1)
            time.sleep(20)

    def delete_snapshot(
        self, project_id: str, snapshot_id: str
    ) -> requests.models.Response:
        """Deletes a flywheel snapshot of a specific ID from a specific project

        Args:
            project_id: the project to delete the snapshot from
            snapshot_id: the snapshot id to delete

        """

        log.info(f"deleting snapshot {snapshot_id} from project {project_id}")
        result = self.client.delete(
            f"/snapshot/projects/{project_id}/snapshots/{snapshot_id}"
        )
        return result

    def _load_project_str(self, pstring: str) -> Union[fw_utils.dicts.AttrDict, None]:
        """Loads a project given an identification string.

        The identification string can be:
        1. A flywheel ID
        2. A flywheel lookup string
        3. A project label.

        if a label is provided, we assume that the project is in the same group as the source project.

        Args:
            pstring (str): a project ID, lookup string, or label

        Returns:
            Union[fw_utils.dicts.AttrDict, None]: a flywheel project object or None if not found
        """
        # First, if the string matches the format of a project ID, we can try to get the project directly
        if FlywheelUtils.is_id(pstring):
            project = self._get_project(pstring)
        # If not, hopefully a lookup is provided including the group, and we can find the project that way.
        elif FlywheelUtils.is_lookup(pstring):
            project = self._lookup_project(pstring)
        # Otherwise, we assume it is a project label and try to find it in the same group as the source project.
        else:
            # If we don't have the source project set yet, someone is trying to set the source project using
            # just a project label.  In the words of Captain Picard, NOT GOOD ENOUGH!  We must be able to
            # at least assume that the group is the same as the source project.
            if self._source_project is None:
                log.error(
                    "Source project not set.  A group must be provided using a lookup string"
                )
                return None
            # Assume the group is that of the source project.  We're not going to be searching for ANY
            # project with a given label.
            group = self._source_project.group
            # Create an appropriately formatted finder filter to search for the project.
            project_filter = "label=" + pstring + ",group=" + group
            project = FlywheelUtils.find_container(
                self.client, "project", project_filter
            )
        return project

    def _get_project(self, project_id: str) -> Union[fw_utils.dicts.AttrDict, None]:
        """Get a project object from the project ID"""
        try:
            result = FlywheelUtils.get_container(
                fw_client=self.client, id_=project_id, container_type="project"
            )
            result.id = result._id
            return result
        except NotFound:
            log.error(f"project with ID {project_id} not found")
            return None

    def _find_project(
        self, project_filter: str
    ) -> Union[fw_utils.dicts.AttrDict, None]:
        """Find a project object from the project filter"""
        try:
            result = FlywheelUtils.find_container(
                fw_client=self.client, container_type="project", filter=project_filter
            )
            result.id = result._id
            return result
        except NotFound:
            log.error(f"project matching filter {project_filter} not found")
            return None

    def _lookup_project(
        self, project_lookup: str
    ) -> Union[fw_utils.dicts.AttrDict, None]:
        """Lookup a project object from the project lookup"""
        parts = FlywheelUtils.breakout_lookup(project_lookup)
        if len(parts) != 2:
            log.error(f"Invalid project lookup {project_lookup}")
            return None
        try:
            result = FlywheelUtils.lookup_container(
                fw_client=self.client, lookup=project_lookup
            )
            result.id = result._id
            return result
        except NotFound:
            log.error(f"project matching lookup {project_lookup} not found")
            return None

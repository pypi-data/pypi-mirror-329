import json
import logging
import re
from typing import Union

import flywheel
import fw_utils
from fw_client import FWClient

log = logging.getLogger()

# The regex formula to determine if a string is in the format of a flywheel container ID or not
CONTAINER_ID_FORMAT = "^[0-9a-fA-F]{24}$"

# A union of all container types in flywheel, including what gets returned from
# fw_client, which is an AttrDict
AnyContainer = Union[
    flywheel.Group,
    flywheel.Project,
    flywheel.Subject,
    flywheel.Session,
    flywheel.Acquisition,
    flywheel.AnalysisOutput,
    flywheel.FileEntry,
    fw_utils.dicts.AttrDict,
]

# An ordered list of the primary hierarchy (analysis is not included).
# This is used to see if one container type is the parent or child or another.
PRIMARY_HIERARCHY = ["group", "project", "subject", "session", "acquisition", "file"]
# An ordered list of the full hierarchy (analysis is included).
FULL_HIERARCHY = [
    "group",
    "project",
    "subject",
    "session",
    "acquisition",
    "analysis",
    "file",
]

# In fw_client, api endpoints use the plural form of containers (project -> projects, etc).
# Normally we can just add an s to a given container type to get the endpoint, however
# we have irregular plurals such as analysis that must be addressed.
IRREGULAR_PLURALS = {"analysis": "analyses"}


def is_parent_child(parent: str, child: str) -> bool:
    """determine if `parent` level is a direct parent of `child` level

    Uses the ordered lists

    Args:
        parent: the parent level to test with
        child: the child level to test with

    Returns:
        True if `parent` is parent type of `child`

    """

    # Exceptions to the hierarchy:
    if child == "file":
        # Files cannot be children of groups
        if parent == "group":
            return False
        # Files can be children to everything else
        return True
    if child == "analysis":
        # Analyses cannot be children to a group, analysis, or file.
        if parent in ["group", "analysis", "file"]:
            return False
        # Analyses can be children to everything else.
        return True

    # Primary calculation, is the child directly below the parent?
    ip = PRIMARY_HIERARCHY.index(parent)
    ic = PRIMARY_HIERARCHY.index(child)

    if ic - ip == 1:
        return True
    return False


def get_label(container: AnyContainer) -> str:
    """gets the label or name of a container or file

    Unifies the method to obtain the label or name of a container or file.
    Useful for programatically working with arbitrary flywheel objects.

    Args:
        container: flywheel container or file

    Returns:
        the label or name string

    """
    if "label" in container:
        return container.get("label")
    else:
        return container.get("name")


def get_id(container: AnyContainer) -> str:
    """gets the id of a container or file

    Unifies the method to obtain the indexable id of a container or file.
    Useful for programatically working with arbitrary flywheel objects.

    Args:
        container: flywheel container or file

    Returns:
        the id

    """
    if "file_id" in container or container.get("container_type") == "file":
        return container.get("file_id")
    return container.get("_id", container.get("id"))


def make_plural(element: str) -> str:
    """Makes common flywheel object levels plural, accounting for irregulars.

    Used for calling api endpoints using the fw_client library.

    Args:
        element: the container level/flywheel element to pluralize

    Returns:
        the plural string of `element`

    """
    return IRREGULAR_PLURALS.get(element, f"{element}s")


def get_child(level: str) -> str:
    """Returns the immediate child of a given level in the hierarchy

    Args:
        level (str): The level to get the immediate child of

    Returns:
        str: the immediate child level
    """
    if level == PRIMARY_HIERARCHY[-1] or level not in PRIMARY_HIERARCHY:
        return None

    i = PRIMARY_HIERARCHY.index(level)
    return PRIMARY_HIERARCHY[i + 1]


def get_parent(level: str) -> str:
    """Returns the immediate parent of a given level in the hierarchy

    Args:
        level (str): the level to get the immediate parent of

    Returns:
        str: the immediate parent level
    """

    if level == PRIMARY_HIERARCHY[0] or level not in PRIMARY_HIERARCHY:
        return None

    i = PRIMARY_HIERARCHY.index(level)
    return PRIMARY_HIERARCHY[i - 1]


def get_container_type(container):
    """Extract the container type of a dictionary-formatted flywheel object"""

    if "file_id" in container or "parent_ref" in container:
        return "file"
    if "job" in container or "gear_info" in container:
        return "analysis"

    parents = container["parents"]
    if "session" in parents:
        container_type = "acquisition"
    elif "subject" in parents:
        container_type = "session"
    elif "project" in parents:
        container_type = "subject"
    elif "group" in parents:
        container_type = "project"
    else:
        container_type = "group"
    return container_type


def get_container(fw_client: FWClient, id_: str, container_type: str = None) -> dict:
    """makes an api get request for a container by ID

    Args:
        fw_client: the flywheel api client
        container_type: the container level to get
        id_: the id of the container

    Returns:
        container: flywheel container.

    """
    if container_type is None:
        endpoint = f"/api/containers/{id_}"
    else:
        endpoint = f"/api/{make_plural(container_type)}/{id_}"
    container = fw_client.get(endpoint)
    return container


def find_container(fw_client: FWClient, container_type: str, filter: str = "") -> dict:
    """makes an api get request to search for a container with filters

    Args:
        fw_client: the flywheel api client
        level: the container level to get
        filter: the filter to apply to the query

    Returns:
        container: flywheel container.

    """
    if container_type is None:
        endpoint = "/api/containers/find"
    else:
        endpoint = f"/api/{make_plural(container_type)}"
    container = fw_client.get(endpoint, params={"filter": filter})
    return container


def lookup_container(fw_client: FWClient, lookup: str) -> dict:
    """makes an api get request for a container by lookup string"""

    parts = breakout_lookup(lookup)
    container = fw_client.post("/api/lookup", data=json.dumps({"path": parts}))
    return container


def is_id(id_: str) -> bool:
    """determine if a string is in the format of a flywheel container ID

    Args:
        id_: the string to test

    Returns:
        True if the string is in the format of a flywheel container ID

    """
    return re.match(CONTAINER_ID_FORMAT, id_) is not None


def is_lookup(lookup: str) -> bool:
    """determine if a string is in the format of a flywheel container lookup

    This is a bit silly if I'm being honest:
    Technically a flywheel path follows the following format:
    `fw://<group>/<project>/<subject>/<session>/<acquisition>/<file>`
    This is how your group/project label is displayed in the UI, with the `fw://` prefix.
    However when you use the "lookup" function of the SDK, you CAN NOT include the fw:// prefix.

    So, I am unsure if users will include this or not, based on how it looks in the UI vs how
    it's actually used in practice.

    Because of this, I'm going to NOT require it start with `fw://` to work, because
    strictly speaking it doesn't need it.

    As an edge case, it is possible to create a container with a "/" character in the label.
    So yes, if your project label is "project/label", and you pass this in to "is_lookup",
    then it will erroneously return True.

    HOWEVER, in this case, lookups are completely broken anyway.  There is no possible way to
    use a lookup with a "/" in the label, because the "/" is used to separate the parts of the lookup.

    Since the use of a "/" in the label ruins ALL lookups, you shouldn't be using this method anyway.

    So yes, if it has a "/" we assume it's a lookup.  Simple as that.

    Args:
        lookup: the string to test

    Returns:
        True if the string is in the format of a flywheel container lookup

    """
    return "/" in lookup


def breakout_lookup(lookup: str) -> tuple:
    """breaks out a lookup string into its parts

    Args:
        lookup: the lookup string to break out

    Returns:
        tuple: the parts of the lookup string

    """
    if lookup.startswith("fw://"):
        lookup = lookup[5:]
    parts = lookup.split("/")
    return parts

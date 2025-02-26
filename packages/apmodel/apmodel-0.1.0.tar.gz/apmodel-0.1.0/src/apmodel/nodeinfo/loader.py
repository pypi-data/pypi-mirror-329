from typing import Union, Optional

from .ni20.nodeinfo import NodeInfo as nodeinfo20
from .ni21.nodeinfo import NodeInfo as nodeinfo21


def load(data: dict) -> Optional[Union[nodeinfo20, nodeinfo21]]:
    version = data.get("version")
    if not version:
        return None
    elif version == "2.0":
        return nodeinfo20.from_dict(data)
    elif version == "2.1":
        return nodeinfo21.from_dict(data)
    else:
        return None
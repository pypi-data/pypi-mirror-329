from ._http_client import HttpClient
from .tool import Tool


def update_tool(*, client: HttpClient, params: Tool) -> Tool:
    """update_tool updates an existing tool. It allows callers to convert mock tools
    into real tools, but not the other way around.

    Note: requires a `Management` API key."""
    rsp = client.put(
        path="tools/{tool_id}",
        body=params.to_dict(),
    )

    return Tool.from_dict(rsp)

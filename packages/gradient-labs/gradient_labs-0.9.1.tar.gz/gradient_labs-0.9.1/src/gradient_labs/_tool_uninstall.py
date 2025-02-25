from ._http_client import HttpClient


def uninstall_tool(*, client: HttpClient, tool_id: str) -> None:
    """uninstall_tool deletes a tool by uninstalling it. Note: this does not
    (yet) check whether those tools are used in procedures. Use with caution!

    Note: requires a `Management` API key."""
    _ = client.delete(
        path=f"tools/{tool_id}",
        body={},
    )

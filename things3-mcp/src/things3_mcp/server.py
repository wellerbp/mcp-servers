"""Things 3 MCP Server — capture todos from Claude sessions without context-switching."""

import json
import os
import subprocess
from urllib.parse import quote

from mcp.server.fastmcp import FastMCP

# Auto-detect Things DB, allow override via env var.
# things-py finds it automatically in most cases; the env var handles
# non-standard paths (e.g. ThingsData-XXXXX subdirectories).
THINGS_DB = os.environ.get("THINGS_DB", None)

mcp = FastMCP("Things 3")


def _things_url(payload: list[dict]) -> str:
    """Build a things:///json URL from a payload array."""
    return f"things:///json?data={quote(json.dumps(payload))}"


def _open_url(url: str) -> None:
    """Open a URL on macOS."""
    subprocess.run(["open", url], check=True)


def _db_kwargs() -> dict:
    """Return filepath kwarg for things-py if a custom DB path is set."""
    if THINGS_DB:
        return {"filepath": THINGS_DB}
    return {}


def _things():
    """Lazy import things module."""
    import things

    return things


@mcp.tool()
def add_todo(
    title: str,
    notes: str = "",
    checklist_items: list[str] | None = None,
    project: str = "",
    tags: list[str] | None = None,
    when: str = "",
    deadline: str = "",
) -> dict:
    """Add a todo to Things 3.

    Args:
        title: Todo title (required).
        notes: Additional notes/context.
        checklist_items: Nested checklist items as plain strings.
        project: Project name to file under. Call list_projects first to verify name.
        tags: Tag names. Call list_tags first to match existing tags before creating new ones.
        when: Schedule — "today", "tomorrow", "evening", "someday", "anytime", or YYYY-MM-DD.
        deadline: Due date as YYYY-MM-DD.
    """
    attrs = {"title": title}
    if notes:
        attrs["notes"] = notes
    if checklist_items:
        attrs["checklist-items"] = [
            {"type": "checklist-item", "attributes": {"title": item}}
            for item in checklist_items
        ]
    if project:
        attrs["list"] = project
    if tags:
        attrs["tags"] = tags
    if when:
        attrs["when"] = when
    if deadline:
        attrs["deadline"] = deadline

    payload = [{"type": "to-do", "attributes": attrs}]
    _open_url(_things_url(payload))
    return {"status": "sent", "title": title, "attributes": attrs}


@mcp.tool()
def list_projects() -> list[dict]:
    """List active Things 3 projects. Call before add_todo to verify project names."""
    things = _things()
    projects = things.projects(**_db_kwargs())
    return [
        {
            "title": p.get("title", ""),
            "uuid": p.get("uuid", ""),
            "area": p.get("area_title", ""),
        }
        for p in projects
    ]


@mcp.tool()
def search_todos(query: str) -> list[dict]:
    """Search existing todos in Things 3 by keyword."""
    things = _things()
    results = things.search(query, **_db_kwargs())
    return [
        {
            "title": t.get("title", ""),
            "uuid": t.get("uuid", ""),
            "status": t.get("status", ""),
            "project": t.get("project_title", ""),
            "tags": t.get("tags", []),
        }
        for t in results
    ]


@mcp.tool()
def list_tags() -> list[str]:
    """List all Things 3 tags. Call before add_todo to match existing tags or decide on new ones."""
    things = _things()
    return [t["title"] for t in things.tags(**_db_kwargs())]


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

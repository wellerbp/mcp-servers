# things3-mcp

MCP server for [Things 3](https://culturedcode.com/things/) on macOS.

**Writes** via `things:///json` URL scheme — full support for checklist items, projects, tags, scheduling, and deadlines.

**Reads** via [things-py](https://github.com/thingsapi/things.py) (read-only SQLite access).

## Tools

| Tool | Description |
|------|-------------|
| `add_todo` | Create a todo with title, notes, checklist items, project, tags, when, deadline |
| `list_projects` | List active projects (call before `add_todo` to verify names) |
| `list_tags` | List all tags (call before `add_todo` to match existing tags) |
| `search_todos` | Search todos by keyword |

## Install

```bash
pip install things3-mcp
```

Or run without installing:

```bash
uvx things3-mcp
```

## Claude Code config

Add to your MCP configuration (`~/.claude.json`):

```json
{
  "mcpServers": {
    "things3": {
      "command": "things3-mcp"
    }
  }
}
```

Or with `uvx`:

```json
{
  "mcpServers": {
    "things3": {
      "command": "uvx",
      "args": ["things3-mcp"]
    }
  }
}
```

## Non-standard DB path

If Things uses a non-standard database path (e.g. `ThingsData-XXXXX` subdirectory), set the `THINGS_DB` environment variable:

```json
{
  "mcpServers": {
    "things3": {
      "command": "things3-mcp",
      "env": {
        "THINGS_DB": "/path/to/main.sqlite"
      }
    }
  }
}
```

## Requirements

- macOS (Things 3 is macOS/iOS only)
- Things 3 installed
- Python 3.11+

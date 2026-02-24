# mcp-servers

Personal MCP servers for Claude Code. Feel free to use or modify!

## Servers

| Server | Description |
|--------|-------------|
| [things3-mcp](things3-mcp/) | Things 3 integration with checklist support |

## Install with Nix (flake)

Add as a flake input:

```nix
inputs.mcp-servers = {
  url = "github:wellerbp/mcp-servers";
  inputs.nixpkgs.follows = "nixpkgs";
};
```

Then add the package to your home/system packages:

```nix
mcp-servers.packages.${system}.things3-mcp
```

## Install without Nix

Each server has its own README with `pip`/`uvx` instructions.

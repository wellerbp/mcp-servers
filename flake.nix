{
  description = "Personal MCP servers";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "aarch64-darwin";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3;

      things-py = python.pkgs.buildPythonPackage rec {
        pname = "things-py";
        version = "1.0.0";
        format = "wheel";

        src = pkgs.fetchurl {
          url = "https://files.pythonhosted.org/packages/e4/31/3ac1f88d40a9f03d761e08be9c89f6419b41e8be7941c3909929445df246/things_py-1.0.0-py3-none-any.whl";
          hash = "sha256-m8bKAg9J82hq6c0qYQyo8Ai9mQxtCLF7PrgMLrGdz2k=";
        };
      };

      things3-mcp = python.pkgs.buildPythonApplication {
        pname = "things3-mcp";
        version = "0.1.0";
        pyproject = true;

        src = ./things3-mcp;

        build-system = [ python.pkgs.hatchling ];

        dependencies = [
          python.pkgs.mcp
          things-py
        ];
      };
    in
    {
      packages.${system} = {
        things3-mcp = things3-mcp;
        default = things3-mcp;
      };

      apps.${system}.default = {
        type = "app";
        program = "${things3-mcp}/bin/things3-mcp";
      };
    };
}

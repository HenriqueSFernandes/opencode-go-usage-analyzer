{
  description = "OpenCode Go usage analyzer (CLI + dev shell)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPkgs = pkgs.python3Packages;

        opencodeUsageAnalyzer = pythonPkgs.buildPythonApplication {
          pname = "opencode-go-usage-analyzer";
          version = "0.2.0";
          pyproject = true;
          src = ./.;

          build-system = [
            pythonPkgs.hatchling
          ];

          propagatedBuildInputs = [
            pythonPkgs.beautifulsoup4
            pythonPkgs.requests
            pythonPkgs.rich
          ];

          meta = {
            description = "CLI that displays OpenCode Go workspace usage from the web dashboard";
            homepage = "https://github.com/henriqueSFernandes/opencode-go-usage-analyzer";
            license = pkgs.lib.licenses.mit;
            mainProgram = "opencode-usage";
          };
        };
      in
      {
        packages = {
          default = opencodeUsageAnalyzer;
          opencode-go-usage-analyzer = opencodeUsageAnalyzer;
        };

        apps = {
          default = {
            type = "app";
            program = "${opencodeUsageAnalyzer}/bin/opencode-usage";
          };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            uv
          ];
        };
      });
}

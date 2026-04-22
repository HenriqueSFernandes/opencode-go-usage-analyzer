## opencode-go-usage-analyzer

CLI tool to display OpenCode Go workspace usage limits from the web dashboard.

### Features

- Shows Rolling/Weekly/Monthly usage with a colorized terminal table.
- Interactive authentication prompt (workspace ID + auth token).
- Local session persistence by default.
- `--no-remember` mode for one-off runs without touching local session storage.
- `--logout` to clear the saved local session quickly.

### Requirements

- Python 3.10+
- `uv` (recommended) or `pip`

### Install

#### With uv (recommended)

```bash
uv tool install opencode-go-usage-analyzer
```

#### From source

```bash
git clone https://github.com/henriqueSFernandes/opencode-go-usage-analyzer.git
cd opencode-go-usage-analyzer
uv sync
uv run opencode-usage --help
```

#### With Nix (flake)

Run directly without installing:

```bash
nix run github:henriqueSFernandes/opencode-go-usage-analyzer -- --help
```

Install imperatively to your user profile:

```bash
nix profile install github:henriqueSFernandes/opencode-go-usage-analyzer
```

Add to a NixOS or Home Manager flake (declarative):

```nix
# flake.nix
{
  inputs.opencode-go-usage-analyzer.url = "github:henriqueSFernandes/opencode-go-usage-analyzer";

  outputs = { self, nixpkgs, home-manager, opencode-go-usage-analyzer, ... }@inputs: {
    # ...
  };
}
```

Then in your Home Manager configuration:

```nix
{ config, pkgs, inputs, ... }:

{
  home.packages = [
    inputs.opencode-go-usage-analyzer.packages.${pkgs.system}.default
  ];
}
```

### Usage

```bash
opencode-usage
```

On first run, the CLI prompts for:

- Workspace ID
- Auth token (`auth` cookie value)

By default, credentials are saved to `.opencode/session.json` and reused automatically.

### Command options

```bash
opencode-usage --no-remember
opencode-usage --logout
```

- `--no-remember`: do not read or write the local session file.
- `--logout`: delete the local saved session and exit.

### Development

```bash
uv sync --extra dev
uv run opencode-usage --help
uv build
```

### License

MIT. See `LICENSE`.

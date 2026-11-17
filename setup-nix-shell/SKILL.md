---
name: setup-nix-shell
description: Detect the codebase language/framework, identify dependencies, generate a corresponding shell.nix file (and language-specific manifests if missing), and test/verify the nix-shell environment. Use when the user requests environment setup or shell.nix creation.
trigger: /setup-nix-shell
---

# /setup-nix-shell

Scan the codebase, identify required packages and runtime version, write a robust `shell.nix` file (setting up virtualenvs, dependencies, hooks), and verify that it loads correctly.

## Usage

```
/setup-nix-shell         # automatically scan, generate, and verify nix environment
```

## What You Must Do When Invoked

Follow these phases in order. Do not skip phases.

---

## Phase 1 — Scan Codebase and Detect Environment

Scan the workspace directory to understand the project type, language, and required libraries.

**1. List files and look for manifest/source files:**
Check for specific files in the workspace:
- `requirements.txt`, `pyproject.toml`, `setup.py`, `*.py` -> Python
- `package.json`, `yarn.lock`, `package-lock.json`, `pnpm-lock.yaml`, `*.js`, `*.ts` -> Node.js
- `go.mod`, `go.sum`, `*.go` -> Go
- `Cargo.toml`, `Cargo.lock`, `*.rs` -> Rust
- `Gemfile`, `Gemfile.lock`, `*.rb` -> Ruby
- `mix.exs`, `*.ex`, `*.exs` -> Elixir

**2. Parse files for dependencies:**
- For Python: look at `requirements.txt` or read imports from main python files. Check if packages like `flask`, `requests`, `azure-identity` are needed.
- For Node.js: read `package.json` to find runtime version requirements and external tools (e.g. `node`, `yarn`, `pnpm`).
- For Go/Rust: look for minimum required language versions.
- Note any native library dependencies (e.g., `openssl` for crypto/network calls, `git` for vcs/cloning, `libffi` for C bindings, `sqlite` or `postgresql` for databases).

---

## Phase 2 — Confirm Project Type and Dependencies

Present the detected environment to the user and confirm before writing files:

```
I've scanned the codebase and detected:
  - Language/Runtime: Python (python3)
  - Packages identified: flask, python-dotenv, requests, azure-identity, azure-ai-projects
  - Suggested system packages: openssl, git, libffi

Would you like to proceed with generating requirements.txt and shell.nix for this setup? (yes/no)
```

Wait for user confirmation before writing files.

---

## Phase 3 — Generate Manifests & Nix Configuration

### Case A: Python Projects
If no `requirements.txt` exists, write it first containing the discovered dependencies.

Write `shell.nix` using a virtual environment approach so users can install pip packages smoothly on NixOS:

```nix
{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python3Packages;
in
pkgs.mkShell {
  name = "python-project-env";

  buildInputs = [
    pkgs.python3
    pythonPackages.pip
    pythonPackages.virtualenv
    pkgs.openssl
    pkgs.git
    pkgs.libffi
  ];

  shellHook = ''
    # Disable PIP_USER to avoid virtualenv conflicts on NixOS
    export PIP_USER=false

    if [ ! -d ".venv" ]; then
      echo "Creating Python virtual environment in .venv..."
      virtualenv .venv
    fi
    source .venv/bin/activate
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
      echo "Installing Python packages from requirements.txt..."
      pip install -r requirements.txt
    fi
    echo "========================================================="
    echo " Nix Python Environment Loaded successfully "
    echo "========================================================="
  '';
}
```

### Case B: Node.js Projects
Create a `shell.nix` that configures `nodejs` and package managers:

```nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "node-project-env";

  buildInputs = [
    pkgs.nodejs
    # pkgs.nodePackages.yarn # uncomment if using yarn
    # pkgs.pnpm            # uncomment if using pnpm
    pkgs.git
    pkgs.openssl
  ];

  shellHook = ''
    echo "========================================================="
    echo " Nix Node.js Environment Loaded successfully "
    echo " Node version: $(node --version)"
    echo "========================================================="
  '';
}
```

### Case C: Go Projects
Create a `shell.nix` with Go tools:

```nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "go-project-env";

  buildInputs = [
    pkgs.go
    pkgs.gopls
    pkgs.git
    pkgs.gcc
  ];

  shellHook = ''
    echo "========================================================="
    echo " Nix Go Environment Loaded successfully "
    echo " Go version: $(go version)"
    echo "========================================================="
  '';
}
```

---

## Phase 4 — Test and Verify the Environment

Run `nix-shell` to test the configuration. For instance, run a dry-run test command to verify everything starts and package commands run successfully:

```bash
nix-shell --run "echo 'Verification: nix-shell starts correctly'"
```

For Python projects, verify imports:
```bash
nix-shell --run "python -c 'import flask; print(\"Verify import: Flask is present\")'"
```

Show the results of the verification to the user.

---

## Error Handling

**"nix-shell: command not found"**: The user doesn't have Nix installed. Inform them they need Nix or NixOS to run this environment.
**"Package build/compilation error inside Nix shell"**: Check if a compiler (`gcc`, `pkg-config`) or dependency library (e.g. `zlib`, `openssl`) is missing from `buildInputs` and add it to `shell.nix`.

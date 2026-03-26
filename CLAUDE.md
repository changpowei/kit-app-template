# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

`kit-app-template` is a scaffold for building GPU-accelerated desktop and cloud-streaming applications on the NVIDIA Omniverse Kit SDK. It provides templates for Kit applications (`.kit` files) and extensions (Python or C++), along with a `repo.sh`/`repo.bat` toolchain that wraps build, launch, test, and packaging operations.

## Common Commands (Linux)

```bash
# Scaffold a new app or extension interactively
./repo.sh template new

# Add layers (e.g. streaming) to an existing app
./repo.sh template modify

# Build (add -c to clean first, -x to rebuild from scratch)
./repo.sh build
./repo.sh build -c

# Launch a built app (interactive selection)
./repo.sh launch

# Pass args through to the Kit executable
./repo.sh launch -- --clear-cache --clear-data --reset-user

# Run tests (always build first)
./repo.sh test

# Package for distribution (fat or thin)
./repo.sh package
./repo.sh package --thin

# Containerize (Linux only)
./repo.sh package_container

# Show all available tools and flags
./repo.sh -h
```

Replace `repo.sh` with `repo.bat` on Windows.

## Architecture

### Everything is an Extension

In the Kit SDK, everything — including applications — is an extension. A `.kit` file is just a TOML manifest that declares a set of extensions to load and their settings. Application templates produce a `.kit` file; extension templates produce a directory with `config/extension.toml` and Python or C++ source.

### Source Layout After `template new`

```
source/
  apps/              # .kit files for each application you create
  extensions/        # Custom extensions (auto-discovered by Kit build system)
templates/           # Read-only template definitions (apps/ and extensions/)
tools/
  VERSION.md         # Package version string (edit this before packaging)
```

### Three Files Must Stay in Sync

When an application exists, all three of the following must reference its `.kit` file or builds will fail:

1. **`premake5.lua`** — `define_app("my_company.my_app.kit")`
2. **`repo.toml`** — `[repo_precache_exts] apps = [...]`
3. **`source/apps/`** — the actual `.kit` file must be present

`./repo.sh template new` handles all three automatically. Manual `.kit` files require manual updates to all three.

### Extension Naming

Use namespaced, lowercase, alphanumeric names (e.g. `my_company.my_extension`). Avoid top-level names matching Python built-ins (`random`, `sys`, `xml`) as they cause import conflicts.

### Build Artifacts

Build output lands in `_build/`. The build system downloads Kit SDK and extension dependencies from NVIDIA registries on first run. Initial RTX-enabled application startup can take 5–8 minutes for shader compilation.

### Packaging Version

The version embedded in packages comes from `tools/VERSION.md` (not from individual `.kit` files). Edit this file before running `./repo.sh package`.

### Template Internals

Templates live in `templates/apps/` and `templates/extensions/`. Template variables use `{{ variable_name }}` syntax. Which templates are available is controlled by `templates/templates.toml`. The `template new` command records what was applied in `source/rendered_template_metadata.json`, which enables `template modify` to work later.

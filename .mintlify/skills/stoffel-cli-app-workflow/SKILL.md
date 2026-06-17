---
name: stoffel-cli-app-workflow
description: Use the stoffel CLI to init, check, build, compile, run, test, inspect, and troubleshoot Stoffel apps.
license: MIT
compatibility: Requires access to the Stoffel CLI/SDK docs and current app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-cli-app-workflow
  source: Stoffel App Developer Skills
---

# Stoffel CLI App Workflow

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Package assumption: the app-facing crates from `StoffelVM` are expected to be published to crates.io. Prefer public package/install snippets when available. Use local path dependencies only for temporary WIP testing before publication or when testing unreleased framework changes.

## Use when

Use this playbook when building, running, testing, inspecting, or troubleshooting a Stoffel application through the `stoffel` command.

## Current source of truth

- `StoffelVM/crates/stoffel-cli/src/main.rs`
- `StoffelVM/crates/stoffel-cli/src/project.rs`
- `StoffelVM/crates/stoffel-cli/tests/cli.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/input_file.rs`

## Core commands

```sh
stoffel init my-app          # alias: stoffel new my-app
stoffel status --verbose     # alias: stoffel doctor --verbose
stoffel check                # validate source and project MPC settings
stoffel build                # build bytecode under target/debug/
stoffel build --release      # build bytecode under target/release/ and default to O3
stoffel compile src/main.stfl --output target/debug/app.stflb
stoffel compile --disassemble target/debug/app.stflb
stoffel run                  # local MPC simulation by default unless --network/--config is set
stoffel dev --once           # one build+run pass; omit --once for watch mode
stoffel test --verbose       # run no-argument Stoffel test functions
stoffel clean --dry-run
stoffel update --check       # alias: stoffel upgrade --check
```

`stoffel run`, `build`, and `compile` accept a project directory, source directory, single `.stfl` file, or existing `.stflb` depending on the command. `build.source` may point at either a file or a source directory; when it is a directory, the CLI recursively compiles all `src/**/*.stfl` files.

## Project config shape

A typical app has `Stoffel.toml`:

```toml
[package]
name = "my-app"
version = "0.1.0"
authors = []

[mpc]
backend = "honeybadger"
parties = 5
threshold = 1
# instance_id = 0
# curve = "bls12_381"       # optional alias: field; mainly for AVSS backend

[build]
source = "src/main.stfl"    # or "src" for a source directory
target_dir = "target"       # alias: output_dir
# optimization_level = 2
```

Rules enforced by the CLI:

- `[package].name` and `[package].version` must be non-empty.
- `package.name` may use only letters, numbers, `-`, and `_`.
- `build.source` must be a relative `.stfl` file path or a relative source directory inside the app.
- `build.target_dir` must be a relative directory inside the app and cannot be under `src/`.
- `optimization_level` must be `0..3`.
- `parties`, `threshold`, and `instance_id` must be unquoted positive whole numbers.
- HoneyBadger requires Byzantine topology: at least `4 * threshold + 1` parties, with the current default of `5` parties and threshold `1`.

## Backend and curve flags

Project config and CLI overrides support:

```sh
stoffel check --backend honeybadger --parties 5 --threshold 1
stoffel build --backend avss:bls12_381
stoffel build --backend avss:bn254
stoffel build --backend avss:curve25519
stoffel build --backend avss:ed25519
stoffel build --backend avss:secp256k1
stoffel build --backend avss:p-256
```

`--protocol` aliases `--backend`; `--curve` aliases `--field` in CLI parsing. HoneyBadger does not take a curve suffix.

## App templates

Use `stoffel init --help` for current template names. Current app-facing templates include:

```sh
stoffel init my-app                         # default Stoffel app + Rust wrapper files
stoffel init my-lib --lib                   # library-style Stoffel source
stoffel init my-rust-app --template rust    # Rust app wrapper with nested stoffel/ project
stoffel init my-python-app --template python
stoffel init my-foundry-app --template solidity-foundry
stoffel init my-hardhat-app --template solidity-hardhat
```

Treat non-Rust wrapper templates as integration placeholders until their public SDKs/docs are published.

## Inputs

Named function inputs use repeated `--input` flags:

```sh
stoffel run src/main.stfl --input a=40 --input b=2
```

ClientStore inputs use repeated `--client-input` flags. Repeating the same slot appends values in order for that client:

```sh
stoffel run examples/mpc_top_k/main.stfl \
  --client-input 0=50 --client-input 0=20 --client-input 0=40 \
  --client-input 0=10 --client-input 0=30 \
  --expected-output-clients 1
```

Do not pass comma-separated assignments like `--input a=1,b=2`.

## Input files

Both named inputs and ClientStore inputs can be loaded from `.json`, `.csv`, or `.txt`.

Named inputs:

```sh
stoffel run --input-file inputs.json
stoffel run --input-file inputs.csv
stoffel run --input-file inputs.txt
```

Formats:

```json
{"a": 40, "b": 2}
```

```csv
a,b
40,2
```

```txt
# one name=value per line
a=40
b=2
```

ClientStore inputs:

```sh
stoffel run --client-input-file client-inputs.json --expected-output-clients 1
stoffel run --client-input-file client-inputs.csv --expected-output-clients 1
stoffel run --client-input-file client-inputs.txt --expected-output-clients 1
```

Formats:

```json
{"0": [40, 2], "1": [7]}
```

```csv
slot,value
0,40
0,2
1,7
```

```txt
# repeated slots append in order
0=40
0=2
1=7
```

Values may be integers, unsigned integers where supported, booleans, strings, JSON arrays/objects, or `0x`-prefixed bytes depending on the execution path.

## Bytecode and inspection

```sh
stoffel build --program-info        # build stats are printed after bytecode write
stoffel run target/debug/app.stflb --program-info
stoffel compile --disassemble target/debug/app.stflb
```

`--program-info` on `run` prints function/instruction metadata and client IO metadata before execution.

## Validation / done criteria

For a CLI workflow change or app setup, collect real output from:

```sh
stoffel status --verbose
stoffel check
stoffel build
stoffel run --timeout-secs 180
```

If tests exist:

```sh
stoffel test --verbose
```

For secret examples copied from the monorepo, use the exact first-line `# run-args:` header when present.

## Common pitfalls

- `stoffel run --config` expects network/off-chain config, not project `Stoffel.toml`.
- `stoffel init` creates a project directory, not a single file.
- If a path already contains `Stoffel.toml`, use `stoffel status` or `stoffel run`; do not re-init unless intentionally refreshing template files with `--force`.
- Do not pass named inputs to ClientStore programs or ClientStore inputs to normal function-argument programs.
- Do not claim a command works unless it was actually run.

## Next playbooks

- Stoffel-Lang App Programming
- Stoffel Secret MPC Programming
- Stoffel Local MPC Dev Loop
- Stoffel App Troubleshooting

---
name: stoffel-app-troubleshooting
description: Diagnose app-level init, check, build, run, local MPC, binding, SDK, and network failures with evidence.
license: MIT
compatibility: Requires access to the Stoffel CLI/SDK docs and current app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-app-troubleshooting
  source: Stoffel App Developer Skills
---

# Stoffel App Troubleshooting

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Package assumption: the app-facing crates from `StoffelVM` are expected to be published to crates.io. Prefer public package/install snippets when available. Use local path dependencies only for temporary WIP testing before publication or when testing unreleased framework changes.

## Use when

Use this playbook when a Stoffel app fails to init, check, build, run, test, execute locally, generate bindings, or connect through the SDK/network path.

## Goal

Diagnose app-level issues systematically and collect real evidence before reporting success.

## First commands

From the app root:

```sh
stoffel status --verbose
stoffel check
stoffel build --program-info
```

If the app has tests:

```sh
stoffel test --verbose
```

If Rust SDK code is involved:

```sh
cargo check
cargo test
```

If local MPC is involved:

```sh
stoffel run --timeout-secs 180 <inputs or documented run-args>
```

## Config checklist

Inspect `Stoffel.toml`:

- `[package]` exists.
- `name` and `version` are non-empty.
- `package.name` uses only letters, numbers, `-`, and `_`.
- `build.source` is relative, inside the project, and either a `.stfl` file or source directory.
- `build.target_dir` is a relative directory, not under `src/`, and not a file path.
- `optimization_level` is `0..3` if present.
- `[mpc].parties`, `[mpc].threshold`, and `[mpc].instance_id` are unquoted positive whole numbers where present.
- Byzantine validation holds: HoneyBadger needs at least `4 * threshold + 1` parties.
- Backend syntax is valid: `honeybadger`, `avss`, `avss:bls12_381`, `avss:bn254`, `avss:curve25519`, `avss:ed25519`, `avss:secp256k1`, `avss:p-256`.
- `curve`/`field` is only used where a backend/curve combination supports it.

## Input checklist

- Named function inputs use repeated `--input NAME=VALUE`.
- ClientStore inputs use repeated `--client-input SLOT=VALUE`.
- Repeating the same ClientStore slot appends values in order for `ClientStore.take_share(slot, index)`.
- Do not combine multiple assignments in one flag.
- Named input names must match function parameters exactly.
- Client slots must be numeric.
- If using input files, extensions must be `.json`, `.csv`, or `.txt`.
- Named JSON inputs are an object like `{"a": 40, "b": 2}`.
- Client JSON inputs are an object keyed by numeric slot like `{"0": [40, 2]}`.
- Client CSV inputs require `slot,value` or `client_slot,value` headers.
- TXT input files use one `name=value` or `slot=value` assignment per line; blank lines and `#` comments are ignored.
- CLI values are integers, booleans, strings/JSON where accepted by file parsing, or `0x`-prefixed bytes where supported.

## Bytecode checklist

- Rebuild `.stflb` after source changes.
- Regenerate typed bindings after bytecode changes.
- Explicit SDK backend/curve must match bytecode metadata. Prefer generated `ProgramManifest` for ClientStore apps.
- Use `--program-info` or disassembly when diagnosing wrong entrypoint/function/client metadata.
- If a source directory is configured, confirm the intended file was compiled; the CLI can compile multiple `.stfl` files.

## Local MPC checklist

- Confirm `stoffel-run` is installed or provide `--runner` / `STOFFEL_RUN_BIN`.
- Confirm the runner binary was built for the execution environment's OS/architecture.
- Increase `--timeout-secs` before declaring protocol failure.
- Avoid concurrent local party meshes that collide on ports/processes.
- Verify whether the app uses named inputs or ClientStore inputs.
- For examples with a first-line `# run-args:` header, copy those exact flags.
- Include `--expected-output-clients N` for programs that call `MpcOutput.send_to_client` or `Share.send_to_client`.

## Typed bindings checklist

- Bindings were generated from the same `.stflb` loaded at runtime.
- Rust code includes generated bindings after generation.
- `cargo check` was run after regeneration.
- If duplicate crate/output collision errors appear while crates are unpublished/path/git based, pre-generate bindings or remove the duplicate SDK build-dependency until published dependencies deduplicate.

## Network/off-chain checklist

- Local smoke passes before network work.
- Network config is not project `Stoffel.toml`.
- Client slot exists in program metadata.
- Generated bindings came from the same `.stflb`.
- Coordinator address, node RPC addresses, timestamp, identity material, and expected certificates are provided.
- Network config validates server addresses, expected parties, expected clients, threshold, backend, and preprocessing.

## Minimal diagnosis report

When handing off a failure, include:

- command run
- working directory
- `stoffel --help`/version if relevant
- app `Stoffel.toml` with secrets removed
- exact error output
- whether `stoffel status --verbose` passed
- whether `stoffel check` passed
- whether bytecode was rebuilt
- whether typed bindings were regenerated
- exact `# run-args:` header if using an example
- local MPC runner path/version if relevant
- network/off-chain config shape with secrets redacted if relevant

## Common pitfalls

- Do not “fix” app issues by editing framework internals unless the task is explicitly a framework bug report.
- Do not report success from a command that was not run.
- Do not leak private client inputs, tokens, identity material, or secrets into notes, logs, Obsidian, HackMD, or public issues.
- Do not store API tokens in `Stoffel.toml`, app repos, Obsidian, or HackMD.

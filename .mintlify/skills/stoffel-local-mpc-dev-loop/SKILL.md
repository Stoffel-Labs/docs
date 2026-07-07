---
name: stoffel-local-mpc-dev-loop
description: Run local MPC smoke tests, ClientStore input flows, hot reload, and SDK local coordinator-backed execution.
license: MIT
compatibility: Requires access to the current Stoffel CLI/SDK docs and app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-local-mpc-dev-loop
  source: Stoffel App Developer Skills
---

# Stoffel Local MPC Dev Loop

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Dependency assumption: use the current public install snippets from these docs. When developing against a local checkout, make that source-based workflow explicit.

## Use when

Use this playbook when an app needs local MPC smoke testing, ClientStore input runs, hot reload, or SDK local coordinator-backed execution.

## Goal

Give developers a repeatable local loop for testing private/MPC apps before any real network deployment. Local MPC is a verification gate, not the production topology.

## Current source of truth

- `crates/stoffel-cli/src/main.rs`
- `crates/stoffel-rust-sdk/README.md`
- `crates/stoffel-rust-sdk/src/runtime.rs`
- `crates/stoffel-lang/examples/README.md`
- `crates/stoffel-lang/examples/**/*.stfl`

## CLI local run

```sh
stoffel run --timeout-secs 180
stoffel run path/to/main.stfl --timeout-secs 180
stoffel run target/debug/app.stflb --program-info --timeout-secs 180
```

Local mode is the default unless `--network` or `--config` is set.

## Hot reload

```sh
stoffel dev --once --timeout-secs 180
stoffel dev --poll-ms 500 --timeout-secs 180
```

Use `--once` for CI/smoke checks and default watch mode during interactive development.

## Input paths

Named function args:

```sh
stoffel run --input a=40 --input b=2
```

```rust
.with_inputs(&[("a", 40_i64), ("b", 2_i64)])
```

ClientStore values:

```sh
stoffel run --client-input 0=40 --client-input 0=2 --expected-output-clients 1
```

```rust
.with_client_input(0, &[40_i64, 2_i64])
.expected_output_clients(1)
```

The CLI also supports `--input-file` and `--client-input-file` for `.json`, `.csv`, and `.txt` inputs. See [Stoffel CLI App Workflow](/developer-skills/stoffel-cli-app-workflow).

## Use example `run-args` headers

Many secret examples include the exact local flags in the first source line:

```stfl
# run-args: --client-input 0=50 --client-input 0=20 --client-input 0=40 --client-input 0=10 --client-input 0=30 --expected-output-clients 1
```

Run by appending those flags:

```sh
stoffel run crates/stoffel-lang/examples/mpc_top_k/main.stfl \
  --client-input 0=50 --client-input 0=20 --client-input 0=40 \
  --client-input 0=10 --client-input 0=30 \
  --expected-output-clients 1 \
  --timeout-secs 180
```

For repeated client slots, order matters: `--client-input 0=50 --client-input 0=20` maps to `ClientStore.take_share(0, 0)` then `ClientStore.take_share(0, 1)`.

## SDK local run

```rust
let result = runtime
    .local_network()
    .entry("main")
    .timeout(std::time::Duration::from_secs(180))
    .run()
    .await?;
```

Builder shortcut:

```rust
let result = Stoffel::compile_file("src/main.stfl")?
    .parties(5)
    .threshold(1)
    .with_client_input(0, &[42_i64])
    .expected_output_clients(1)
    .execute_local()
    .await?;
```

## Recommended local loop

1. Run `stoffel status --verbose` from the app root.
2. Run `stoffel check` to catch syntax/config/type errors.
3. Run `stoffel build --program-info` to inspect bytecode and client IO metadata.
4. Run `stoffel run --timeout-secs 180` with named inputs or documented `# run-args:` flags.
5. If using Rust, run `cargo check` and `cargo run` against the same bytecode/source.
6. Record the exact command/output in the app handoff.
7. Only then move to network/off-chain config with [Stoffel Deployment Runbook](/developer-skills/stoffel-deployment-runbook).

## Validation / done criteria

For app local-MPC work:

```sh
stoffel status --verbose
stoffel check
stoffel build --program-info
stoffel run --timeout-secs 180 <inputs or documented run-args>
```

For framework example validation:

```sh
cd /path/to/stoffel/crates/stoffel-lang
./examples/validate_examples.sh
STOFFEL_PROGRAM_NAME=mpc_runtime_info.stflb ./examples/validate_examples.sh --host-mpc
```

## Common pitfalls

- Compile-only success is not a local MPC smoke test.
- Local MPC success is not production deployment; it only proves the program and app boundary work on the local test network.
- Increase `--timeout-secs` before assuming protocol failure.
- Avoid port/process collisions by serializing tests that spawn local party meshes.
- Keep `ClientStore` inputs separate from named function inputs.
- Do not omit `--expected-output-clients` for examples/programs that send client outputs.
- AVSS support is backend/curve/input dependent; verify the current SDK boundary.

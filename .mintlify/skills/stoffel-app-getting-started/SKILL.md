---
name: stoffel-app-getting-started
description: Install the Stoffel tooling, create a new app, run first local smoke tests, and choose the right development path.
license: MIT
compatibility: Requires access to the Stoffel CLI/SDK docs and current app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-app-getting-started
  source: Stoffel App Developer Skills
---

# Stoffel App Getting Started

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Package assumption: the app-facing crates from `StoffelVM` are expected to be published to crates.io. Prefer public package/install snippets when available. Use local path dependencies only for temporary WIP testing before publication or when testing unreleased framework changes.

## Use when

Use this playbook when a developer or coding agent needs the shortest path from an empty directory to a working Stoffel application.

## Current source of truth

Use the public docs when available, then verify against the current app-facing repo surfaces:

- `StoffelVM/README.md`
- `StoffelVM/crates/stoffel-cli/src/main.rs`
- `StoffelVM/crates/stoffel-cli/src/project.rs`
- `StoffelVM/crates/stoffel-lang/examples/README.md`
- `StoffelVM/crates/stoffel-rust-sdk/README.md`

These are source-inspection references for app behavior, not instructions for app developers to edit framework internals.

## Prerequisites

- Rust stable and Cargo.
- The `stoffel` CLI, installed from crates.io once published.
- During WIP only: a local checkout of the `StoffelVM` monorepo branch that contains the app-facing crates.
- For local MPC execution: a `stoffel-run` helper binary available through `PATH`, `--runner`, `STOFFEL_RUN_BIN`, or the SDK builder.

## Install

Preferred public flow after publication:

```sh
cargo install stoffel-cli
stoffel --help
```

Temporary WIP/local checkout flow before publication:

```sh
cd /path/to/StoffelVM
cargo install --path crates/stoffel-cli
cargo build -p stoffel-vm --bin stoffel-run
stoffel --help
```

## Create the first app

```sh
stoffel init my-stoffel-app
cd my-stoffel-app
stoffel status --verbose
stoffel check
stoffel build
stoffel run --timeout-secs 180
```

The default project template includes a Rust wrapper as well as `.stfl` source. For that wrapper, also run:

```sh
cargo build
cargo run
```

## Know the app shape

A new app normally has:

- `Stoffel.toml`: app metadata, default source path, output target dir, and local MPC defaults.
- `src/main.stfl`: the Stoffel program.
- `target/debug/*.stflb`: compiled bytecode after `stoffel build`.
- Optional wrapper files (`Cargo.toml`, `src/main.rs`, `src/stoffel_bindings.rs`) when using the default or Rust templates.

`Stoffel.toml` is a project/build config. It is not the network/off-chain client config passed to `stoffel run --network --config`.

## Choose a development path

- CLI-only path: mostly `.stfl` source and local smoke tests.
- Rust SDK path: embedding compilation/execution, creating clients/servers, generating typed client IO bindings, or integrating with a Rust service.
- Local MPC path: private/secret programs that need real local party execution before network/off-chain work.
- Network/off-chain path: advanced client/server/coordinator integration after the local smoke passes.

## Fast examples to inspect

- Clear language basics: `crates/stoffel-lang/examples/local_control_flow`, `local_collections`, `local_text_processing`.
- First private input flow: `crates/stoffel-lang/examples/mpc_client_private_score`.
- ClientStore gallery with run commands: `crates/stoffel-lang/examples/bits/secret/*`, `matrix/secret/*`, `polynomials/secret/*`, `number_theory/secret/*`, and the app-level `mpc_*` algorithm examples.

Many secret examples now include a first-line `# run-args:` header. Copy those flags when running the example locally.

## Validation / done criteria

A first-app task is complete only when real output has been collected from:

```sh
stoffel status --verbose
stoffel check
stoffel build
stoffel run --timeout-secs 180
```

For Rust wrapper apps, also collect output from:

```sh
cargo build
cargo run
```

For a secret ClientStore example, include its documented `# run-args:` flags and `--expected-output-clients` if present.

## Common pitfalls

- Do not teach monorepo path dependencies as the default after crates are published.
- Do not describe `StoffelVM` internals unless they explain public app behavior.
- Do not claim local MPC works until a real run has completed.
- Do not treat `Stoffel.toml` as network/off-chain config.
- Do not omit `--expected-output-clients` when running examples that send outputs to clients.

## Next playbooks

- Stoffel CLI App Workflow
- Stoffel-Lang App Programming
- Stoffel Secret MPC Programming
- Stoffel Rust App SDK

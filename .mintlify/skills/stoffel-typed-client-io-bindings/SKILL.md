---
name: stoffel-typed-client-io-bindings
description: Generate and use Rust typed client input/output bindings from exact Stoffel bytecode manifests.
license: MIT
compatibility: Requires access to the current Stoffel CLI/SDK docs and app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-typed-client-io-bindings
  source: Stoffel App Developer Skills
---

# Stoffel Typed Client IO Bindings

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Dependency assumption: use public crates.io releases by default, a full pinned revision of the official repository as fallback, and local paths only in explicit nonportable framework-development mode.

## Use when

Use this playbook when a Stoffel app uses `ClientStore` and a Rust client/server wants compile-time input/output structs generated from the exact app bytecode.

## Goal

Generate Rust bindings from the exact `.stflb` program the app will execute, use those bindings for typed client IO, and let the manifest select/validate backend and client-slot IO shape.

## Current source of truth

- `crates/stoffel-rust-sdk/src/codegen.rs`
- `crates/stoffel-rust-sdk/src/types.rs`
- `crates/stoffel-rust-sdk/src/program.rs`
- `crates/stoffel-rust-sdk/src/client.rs`
- `crates/stoffel-rust-sdk/tests/sdk_usage.rs`
- `crates/stoffel-rust-sdk/tests/compile_fail.rs`

## Cargo dependency roles

The runtime SDK belongs in `[dependencies]`; the dedicated generator belongs in `[build-dependencies]`. Use the matching versions from the current Rust SDK installation docs:

```toml
[dependencies]
stoffel = { package = "stoffel-rust-sdk", version = "<current-docs-version>" }

[build-dependencies]
stoffel-bindgen = "<current-docs-version>"
```

If the required API is not published, pin both crates to the same full commit in the official repository:

```toml
[dependencies]
stoffel = { package = "stoffel-rust-sdk", git = "https://github.com/Stoffel-Labs/stoffel.git", rev = "<full-40-character-commit-sha>" }

[build-dependencies]
stoffel-bindgen = { git = "https://github.com/Stoffel-Labs/stoffel.git", rev = "<full-40-character-commit-sha>" }
```

Do not put `stoffel-rust-sdk` in `[build-dependencies]` to generate bindings. Do not emit local `path = "../stoffel/..."` entries except in explicitly labeled, nonportable framework-development manifests.

## Mode A: exact-bytecode bindings

Use this mode for deployment and whenever bindings must describe a specific `.stflb` artifact. Keep the artifact under the app repository (for example `artifacts/program.stflb`), and generate only into Cargo's `OUT_DIR`:

```rust
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let manifest_dir = PathBuf::from(std::env::var_os("CARGO_MANIFEST_DIR").ok_or("missing CARGO_MANIFEST_DIR")?);
    let bytecode = manifest_dir.join("artifacts/program.stflb");
    let out_file = PathBuf::from(std::env::var_os("OUT_DIR").ok_or("missing OUT_DIR")?)
        .join("stoffel_bindings.rs");

    println!("cargo:rerun-if-changed={}", bytecode.display());
    stoffel_bindgen::generate_bindings(&bytecode, &out_file)?;
    Ok(())
}
```

Include the generated file:

```rust
include!(concat!(env!("OUT_DIR"), "/stoffel_bindings.rs"));
```

For non-standard crate paths or derives, call `stoffel_bindgen::generate_bindings_with_config` with the same rooted input/output paths and `stoffel_bindgen::BindingsConfig`.

Runtime code must load the same artifact without assuming the process CWD:

```rust
let bytecode = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
    .join("artifacts/program.stflb");
let runtime = stoffel::Stoffel::load_file(bytecode)?
    .manifest::<ProgramManifest>()
    .build()?;
```

## Mode B: source-generated bindings

Use source mode only when the application intentionally compiles source during its Cargo build. It is convenient for development but does **not** prove that bindings match a separately deployed bytecode file:

```rust
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let manifest_dir = PathBuf::from(std::env::var_os("CARGO_MANIFEST_DIR").ok_or("missing CARGO_MANIFEST_DIR")?);
    let source = manifest_dir.join("stoffel/src/program.stfl");
    let out_file = PathBuf::from(std::env::var_os("OUT_DIR").ok_or("missing OUT_DIR")?)
        .join("stoffel_bindings.rs");

    println!("cargo:rerun-if-changed={}", source.display());
    stoffel_bindgen::generate_bindings_from_source(
        &source,
        &out_file,
        stoffel_bindgen::BindingsConfig::default(),
    )?;
    Ok(())
}
```

Emit one `cargo:rerun-if-changed=...` line for every imported source or other generator input. If the bytecode is built by a separate command, do not blur the modes: build it first, then use exact-bytecode mode against that output.

## Generated shapes

The generator emits:

- `ProgramManifest`
- `impl stoffel::GeneratedProgramManifest for ProgramManifest`
- `Client{slot}Inputs` for each client slot with declared inputs
- `Client{slot}Outputs` for each client slot with declared outputs
- ordered fields such as `input_0`, `input_1`, `output_0`
- `TypedClientInputs` / `TypedClientOutputs` implementations

Current type mapping:

- integer shares -> `i64`
- boolean secret integers -> `bool`
- fixed-point shares -> `f64`

Bindings can be generated for bytecode without ClientStore IO; the file still contains a `ProgramManifest` and a comment that no client IO was declared.

## Use manifest-backed config

```rust
let mpc = stoffel::MpcConfig::builder()
    .manifest::<ProgramManifest>()
    .build()?;

let app_root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
let runtime = stoffel::Stoffel::load_file(app_root.join("program.stflb"))?
    .manifest::<ProgramManifest>()
    .build()?;
```

The manifest carries the bytecode backend plus per-client input/output types. Prefer it over hand-written backend/curve literals for ClientStore programs.

## Typed client call

```rust
let outputs: Client0Outputs = client
    .run_typed(Client0Inputs {
        input_0: 42_i64,
    })
    .await?;
```

Advanced explicit manifest call:

```rust
let outputs = client
    .run_typed_with_manifest::<ProgramManifest, Client0Inputs, Client0Outputs>(inputs)
    .await?;
```

## Bytecode must be the contract

Treat `.stflb` as the app/client contract:

1. Write or update `.stfl` source.
2. Build bytecode with the same backend/curve/topology assumptions that will be used at runtime.
3. Generate Rust bindings from that bytecode.
4. Compile the Rust client/server code.
5. At runtime, load the same bytecode and validate manifest/client IO shape before submitting inputs.

If source changes, rebuild bytecode and regenerate bindings. Do not hand-edit generated structs.

## Multi-client and ordered-input guidance

If a program has:

```stfl
var a = ClientStore.take_share(0, 0)
var b = ClientStore.take_share(0, 1)
var c = ClientStore.take_share(1, 0)
```

Expect generated shapes like:

```rust
Client0Inputs { input_0: ..., input_1: ... }
Client1Inputs { input_0: ... }
```

In the CLI equivalent, repeat a client slot in the same order:

```sh
stoffel run program.stflb \
  --client-input 0=40 --client-input 0=2 \
  --client-input 1=7 \
  --expected-output-clients 2
```

## Validation / done criteria

- Regenerate bindings after bytecode changes.
- Commit the generated app's `Cargo.lock`; run `cargo check --locked` to catch type mismatches.
- Run the app's local smoke with the same bytecode.
- For network/off-chain submissions, validate the runtime's program manifest against generated types before submitting.

Audit dependency provenance without relying on the current directory:

```sh
APP_MANIFEST="/absolute/path/to/client/Cargo.toml"
cargo metadata --locked --format-version 1 --manifest-path "$APP_MANIFEST" \
  > "${APP_MANIFEST%/*}/cargo-metadata.json"
```

Both `stoffel-rust-sdk` and `stoffel-bindgen` must resolve from `registry+...` or the same pinned official `git+...#<full-sha>`. A `null` package source is a local path/workspace leak. Final proof is `cargo check --locked --manifest-path ...` from a clean checkout outside the Stoffel repository, with no adjacent framework checkout.

Framework tests:

```sh
cargo test --locked -p stoffel-rust-sdk generate_bindings_emits_typed_client_io_from_stflb_manifest
cargo test --locked -p stoffel-rust-sdk generated_bindings_type_check_federated_average_example
cargo test --locked -p stoffel-rust-sdk --test compile_fail
```

## Common pitfalls

- Bindings must come from the exact `.stflb` deployed/executed.
- Rebuild bytecode and regenerate bindings after any source, backend, or curve change.
- Do not hand-edit generated binding files.
- Do not bypass manifest validation when network clients submit real inputs.
- Do not assume slot order from Rust struct field order alone; it follows ordered ClientStore metadata from bytecode.
- Wrong: `stoffel = { path = "../stoffel/crates/stoffel-rust-sdk" }` in a distributable app. Right: crates.io, or the official Git URL plus full `rev`.
- Wrong: `stoffel::generate_bindings(...)` from an SDK build-dependency. Right: `stoffel_bindgen` in `[build-dependencies]`.
- Wrong: input/output paths relative to process CWD or generated files written into `src/`. Right: inputs under `CARGO_MANIFEST_DIR`, outputs under `OUT_DIR`, and explicit rerun directives.
- Wrong: generating from source and claiming an independently built deployment artifact is identical. Use exact-bytecode mode for that claim.

## Next playbooks

- [Stoffel App Network and Off-Chain Integration](/developer-skills/stoffel-app-network-and-offchain-integration)
- [Stoffel Local MPC Dev Loop](/developer-skills/stoffel-local-mpc-dev-loop)
- [Stoffel App Troubleshooting](/developer-skills/stoffel-app-troubleshooting)

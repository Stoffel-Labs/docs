---
name: stoffel-typed-client-io-bindings
description: Generate and use Rust typed client input/output bindings from exact Stoffel bytecode manifests.
license: MIT
compatibility: Requires access to the Stoffel CLI/SDK docs and current app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-typed-client-io-bindings
  source: Stoffel App Developer Skills
---

# Stoffel Typed Client IO Bindings

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Package assumption: the app-facing crates from `StoffelVM` are expected to be published to crates.io. Prefer public package/install snippets when available. Use local path dependencies only for temporary WIP testing before publication or when testing unreleased framework changes.

## Use when

Use this playbook when a Stoffel app uses `ClientStore` and a Rust client/server wants compile-time input/output structs generated from the exact app bytecode.

## Goal

Generate Rust bindings from the exact `.stflb` program the app will execute, use those bindings for typed client IO, and let the manifest select/validate backend and client-slot IO shape.

## Current source of truth

- `StoffelVM/crates/stoffel-rust-sdk/src/codegen.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/types.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/program.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/client.rs`
- `StoffelVM/crates/stoffel-rust-sdk/tests/sdk_usage.rs`
- `StoffelVM/crates/stoffel-rust-sdk/tests/compile_fail.rs`

## Generate bindings in `build.rs`

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let out_dir = std::env::var("OUT_DIR")?;
    stoffel::generate_bindings(
        "program.stflb",
        format!("{out_dir}/stoffel_bindings.rs"),
    )?;
    Ok(())
}
```

Include the generated file:

```rust
include!(concat!(env!("OUT_DIR"), "/stoffel_bindings.rs"));
```

For non-standard crate paths or derives:

```rust
stoffel::generate_bindings_with_config(
    "program.stflb",
    format!("{out_dir}/stoffel_bindings.rs"),
    stoffel::BindingsConfig {
        crate_path: "stoffel".to_owned(),
        derives: vec!["Debug".to_owned(), "Clone".to_owned(), "PartialEq".to_owned()],
    },
)?;
```

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

let runtime = stoffel::Stoffel::load_file("program.stflb")?
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
- Run `cargo check` to catch type mismatches.
- Run the app's local smoke with the same bytecode.
- For network/off-chain submissions, validate the runtime's program manifest against generated types before submitting.

Framework WIP tests:

```sh
cargo test -p stoffel-rust-sdk generate_bindings_emits_typed_client_io_from_stflb_manifest
cargo test -p stoffel-rust-sdk generated_bindings_type_check_federated_average_example
cargo test -p stoffel-rust-sdk --test compile_fail
```

## Common pitfalls

- Bindings must come from the exact `.stflb` deployed/executed.
- Rebuild bytecode and regenerate bindings after any source, backend, or curve change.
- Do not hand-edit generated binding files.
- Do not bypass manifest validation when network clients submit real inputs.
- Do not assume slot order from Rust struct field order alone; it follows ordered ClientStore metadata from bytecode.
- While dependencies are unpublished/path/git based, avoid using the same local SDK as both app dependency and build-dependency if it causes Cargo duplicate-crate/output-collision failures. Pre-generate bindings or use a dedicated build step until published crates deduplicate the graph.

## Next playbooks

- Stoffel App Network and Off-Chain Integration
- Stoffel Local MPC Dev Loop
- Stoffel App Troubleshooting

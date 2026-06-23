---
name: stoffel-rust-app-sdk
description: Embed Stoffel in Rust apps using the SDK for compilation, bytecode loading, local execution, clients, and servers.
license: MIT
compatibility: Requires access to the Stoffel CLI/SDK docs and 0.1.0 app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-rust-app-sdk
  source: Stoffel App Developer Skills
---

# Stoffel Rust App SDK

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Dependency assumption: use the public install snippets from these docs. When developing against a local checkout, make that workflow explicit.

## Use when

Use this playbook when a Rust application embeds Stoffel compilation, bytecode loading, local execution, client/server builders, typed client IO bindings, or network/off-chain integration.

## Current source of truth

- `crates/stoffel-rust-sdk/README.md`
- `crates/stoffel-rust-sdk/src/lib.rs`
- `crates/stoffel-rust-sdk/src/prelude.rs`
- `crates/stoffel-rust-sdk/src/runtime.rs`
- `crates/stoffel-rust-sdk/src/config.rs`
- `crates/stoffel-rust-sdk/src/types.rs`
- `crates/stoffel-rust-sdk/examples/*`

## Dependencies

Use the released SDK dependency when your app does not need a local checkout:

```toml
[dependencies]
stoffel = { package = "stoffel-rust-sdk", version = "0.1.0" }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

Use a local checkout when your app needs SDK source or unreleased workspace changes:

```toml
[dependencies]
stoffel = { package = "stoffel-rust-sdk", path = "../stoffel/crates/stoffel-rust-sdk" }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

Use `use stoffel::prelude::*;` for app code.

## Clear local execution

```rust
use stoffel::prelude::*;

fn main() -> stoffel::Result<()> {
    let result = Stoffel::compile(
        "def main(a: int64, b: int64) -> int64:\n  return a + b",
    )?
    .with_inputs(&[("a", 42_i64), ("b", 58_i64)])
    .execute_clear()?;

    assert_eq!(result[0].as_i64(), Some(100));
    Ok(())
}
```

## Local MPC execution

Install the runner used by local coordinator-backed execution from crates.io:

```sh
cargo install stoffel-vm-runner
stoffel-run --help
```

```rust
use stoffel::prelude::*;

#[tokio::main]
async fn main() -> stoffel::Result<()> {
    let result = Stoffel::compile(
        "def main() -> int64:\n  var share = ClientStore.take_share(0, 0)\n  return share.open()",
    )?
    .parties(5)
    .threshold(1)
    .local_runner_path("$HOME/.cargo/bin/stoffel-run")
    .with_client_input(0, &[42_i64])
    .execute_local()
    .await?;

    assert_eq!(result[0].as_i64(), Some(42));
    Ok(())
}
```

If the program sends outputs to client slots, configure the expected output clients before executing:

```rust
let result = Stoffel::compile_file("src/main.stfl")?
    .expected_output_clients(2)
    .with_client_input(0, &[40_i64])
    .with_client_input(1, &[2_i64])
    .execute_local()
    .await?;
```

The SDK can also use `STOFFEL_RUN_BIN` or `.local_runner_path(...)` / local-network builder runner paths. Build the runner for the same OS/architecture where it will execute.

## Loading and saving bytecode

```rust
let runtime = Stoffel::compile_file("src/main.stfl")?.build()?;
runtime.save_bytecode("target/debug/app.stflb")?;
let summary = runtime.bytecode_summary()?;

let loaded = Stoffel::load_file("target/debug/app.stflb")?.build()?;
println!("functions: {:?}", summary.program.function_names);
```

## Builder options to know

Program source:

- `Stoffel::compile(source)`
- `Stoffel::compile_file(path)`
- `Stoffel::load(bytes)`
- `Stoffel::load_file(path)`

MPC config:

- `.parties(n)`
- `.threshold(t)`
- `.instance_id(id)`
- `.honeybadger()`
- `.avss(Curve::Bls12_381)` / `.curve(curve)`
- `.backend(MpcBackend::...)`
- `.manifest::<ProgramManifest>()` when using generated bindings

Compiler options:

- `.optimize(bool)`
- `.optimization_level(0..=3)`
- `.print_ir(bool)`
- `.compiler_options(CompilationOptions { ... })`

Inputs:

- `.with_input("a", 40_i64)`
- `.with_inputs(&[("a", 40_i64), ("b", 2_i64)])`
- `.with_client_input(0, &[40_i64, 2_i64])`
- `.with_client_inputs(&[(0, vec![...])])`
- `.expected_output_clients(n)`

Runtime:

- `.build()`
- `.summary()` / `runtime.summary()`
- `.to_bytecode()` / `runtime.to_bytecode()`
- `.save_bytecode(path)` / `runtime.save_bytecode(path)`
- `.execute_clear()`
- `.execute_local()`
- `.execute_local_function("entry")` / timeout variants where appropriate
- `runtime.client()`, `runtime.server(party_id)`, `runtime.offchain_client_config(slot)`

## SDK value model

Use `stoffel::Value` at the SDK boundary:

- `Value::I64`, `Value::U64`, `Value::Bool`, `Value::Float`, `Value::String`, `Value::Bytes`, `Value::List`, `Value::Object`, `Value::Unit`.
- Convenience accessors: `as_i64`, `as_u64`, `as_bool`, `as_f64`, `as_str`, `as_bytes`, `as_list`, `as_object`, `is_unit`.

Typed client IO maps current manifest types as:

- integer shares -> `i64`
- unsigned integer shares -> `i64`/integer Rust fields at generated boundary depending on manifest mapping
- boolean secret integers -> `bool`
- fixed-point shares -> `f64`

See Stoffel Typed Client IO Bindings for generated structs and validation.

## Network config builders

For deployment-oriented code, use builders instead of hand-rolled maps:

```rust
let config = NetworkConfig::builder()
    .party_id(0)
    .bind_address("127.0.0.1:19200")
    .expected_parties(5)
    .expected_clients(1)
    .peers([
        (1, "127.0.0.1:19201"),
        (2, "127.0.0.1:19202"),
        (3, "127.0.0.1:19203"),
        (4, "127.0.0.1:19204"),
    ])
    .threshold(1)
    .honeybadger()
    .consensus_timeout(std::time::Duration::from_secs(60))
    .preprocessing(1000, 500)
    .build()?;

config.validate_server_addresses()?;
let server = StoffelServer::builder(0).network_config(&config).build()?;
let client = StoffelClient::builder().network_config(&config).build()?;
```

## Validation / done criteria

For Rust app setup:

```sh
cargo check
cargo test
cargo run
```

For local MPC app paths:

```sh
cargo install stoffel-vm-runner
cargo run
```

0.1.0 framework validation:

```sh
cargo test -p stoffel-rust-sdk
cargo run -p stoffel-rust-sdk --example quickstart
cargo run -p stoffel-rust-sdk --example local_mpc_client_input
```

## Common pitfalls

- Do not use path dependencies as the default after crates.io publication.
- Do not simulate protocol behavior in app code; use SDK/runtime execution paths.
- Do not set an explicit backend that conflicts with bytecode metadata. Prefer generated manifests for ClientStore programs.
- For `ClientStore` apps, validate client input shapes before network submission.
- If source is shared between host and container/VM/remote environments, confirm that `stoffel-run` was built for the execution environment.
- Using `stoffel-rust-sdk` as both an app dependency and a build-dependency can trigger Cargo duplicate-crate/output-collision errors with path or git dependencies. Prefer runtime SDK metadata validation for sample apps, or pre-generate bindings outside the app build.

## Next playbooks

- Stoffel Typed Client IO Bindings
- Stoffel Local MPC Dev Loop
- Stoffel App Network and Off-Chain Integration

---
name: stoffel-rust-app-sdk
description: Embed Stoffel in Rust apps using the SDK for compilation, bytecode loading, local execution, clients, and servers.
license: MIT
compatibility: Requires access to the current Stoffel CLI/SDK docs and app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-rust-app-sdk
  source: Stoffel App Developer Skills
---

# Stoffel Rust App SDK

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Dependency assumption: application examples use public crates.io releases by default. A pinned official GitHub revision is the fallback when the required public release is unavailable. A local path is an explicit, nonportable framework-development mode only.

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

Use the released SDK dependency from the current Rust SDK installation docs. Keep the placeholder below synchronized with that page rather than copying a release number into this skill:

```sh
cargo add stoffel-rust-sdk --rename stoffel
cargo add tokio --features macros,rt-multi-thread
```

Equivalent manifest shape:

```toml
[dependencies]
stoffel = { package = "stoffel-rust-sdk", version = "<current-docs-version>" }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

If that release does not contain a required fix, pin the official repository to a full 40-character commit SHA (not a branch, tag, or abbreviated SHA):

```toml
[dependencies]
stoffel = { package = "stoffel-rust-sdk", git = "https://github.com/Stoffel-Labs/stoffel.git", rev = "<full-40-character-commit-sha>" }
```

Only framework contributors intentionally testing an adjacent checkout should use a path dependency:

```toml
# NONPORTABLE framework-development mode; never emit this in a distributable app template.
[dependencies]
stoffel = { package = "stoffel-rust-sdk", path = "../stoffel/crates/stoffel-rust-sdk" }
```

Do not use `path = "../stoffel/..."` as an application default, and do not combine `path` with `version` or `git` to make a locally dependent manifest appear portable.

Use `use stoffel::prelude::*;` for app code.

## Path discipline

Rust file APIs resolve relative paths from the process current directory, which may differ under tests, services, IDEs, and CI. Root app-owned paths at the Cargo manifest instead:

```rust
fn app_path(relative: impl AsRef<std::path::Path>) -> std::path::PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(relative)
}
```

Use `app_path("src/main.stfl")`, `app_path("artifacts/program.stflb")`, and similar values with `compile_file`, `load_file`, and bytecode save/load calls. Accept deployment paths as explicit configuration when artifacts live outside the app; never depend on `cd` having been run first.

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

## Production-shaped client integration

For application integration, design toward deployed services and packaged artifacts: build bytecode once, deploy MPC nodes separately, and have client software load deployment config plus typed bindings. Use local MPC as the development smoke path, not the production topology.

```rust
let runtime = Stoffel::load_file(app_path("dist/program.stflb"))?
    .parties(5)
    .threshold(1)
    .honeybadger()
    .build()?;

let offchain = runtime
    .offchain_client_config(0)?
    .coordinator("coordinator.example.com", 31415)
    .timestamp(deployment_timestamp)
    .node_rpc_addresses([
        "node-0.example.com:40000",
        "node-1.example.com:40001",
        "node-2.example.com:40002",
        "node-3.example.com:40003",
        "node-4.example.com:40004",
    ])
    .identity_files("client-0.crt", "client-0.key")
    .build()?;
```

Generated typed bindings should be compiled into the app client or gateway. Production clients should load pinned bytecode/metadata; they should not compile `.stfl` source dynamically for every request.

## Local MPC execution

Use local MPC to verify the privacy-sensitive path before deploying. `.execute_local().await?` spawns a local MPC test network on the developer machine.

```rust
use stoffel::prelude::*;

#[tokio::main]
async fn main() -> stoffel::Result<()> {
    let result = Stoffel::compile(
        "def main() -> int64:\n  var share = ClientStore.take_share(0, 0)\n  return share.open()",
    )?
    .parties(5)
    .threshold(1)
    .with_client_input(0, &[42_i64])
    .execute_local()
    .await?;

    assert_eq!(result[0].as_i64(), Some(42));
    Ok(())
}
```

If the program sends outputs to client slots, configure the expected output clients before executing:

```rust
let result = Stoffel::compile_file(app_path("src/main.stfl"))?
    .expected_output_clients(2)
    .with_client_input(0, &[40_i64])
    .with_client_input(1, &[2_i64])
    .execute_local()
    .await?;
```

## Loading and saving bytecode

```rust
let bytecode = app_path("target/debug/app.stflb");
let runtime = Stoffel::compile_file(app_path("src/main.stfl"))?.build()?;
runtime.save_bytecode(&bytecode)?;
let summary = runtime.bytecode_summary()?;

let loaded = Stoffel::load_file(&bytecode)?.build()?;
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

See [Stoffel Typed Client IO Bindings](/developer-skills/stoffel-typed-client-io-bindings) for generated structs and validation.

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

For full deployment handoff, also capture coordinator address, node RPC addresses, identity material, bytecode hash, generated binding version, persistence/state location, and process supervision. See [Stoffel Deployment Runbook](/developer-skills/stoffel-deployment-runbook).

## Validation / done criteria

For a generated or handed-off Rust app, commit `Cargo.lock` and use the locked graph in verification and CI:

```sh
cargo generate-lockfile
cargo check --locked
cargo test --locked
cargo run --locked
```

Audit both the manifest text and Cargo's resolved provenance. Run these from the app manifest explicitly, so the result does not depend on the caller's current directory:

```sh
APP_MANIFEST="/absolute/path/to/my-app/Cargo.toml"
test -f "${APP_MANIFEST%/*}/Cargo.lock"
grep -nE 'stoffel-rust-sdk|stoffel-bindgen|path[[:space:]]*=' "$APP_MANIFEST"
cargo metadata --locked --format-version 1 --manifest-path "$APP_MANIFEST" > "${APP_MANIFEST%/*}/cargo-metadata.json"
```

Inspect the Stoffel packages in `cargo-metadata.json`: crates.io packages have a `registry+...` source; the fallback has a `git+https://github.com/Stoffel-Labs/stoffel.git?...#<full-sha>` source. A `null` source means a path/workspace package and fails the portable-app audit.

The final portability proof must run from a clean checkout outside the Stoffel framework repository and without an adjacent `../stoffel` directory:

```sh
APP_REPO_URL="<app-repository-url>"
PROOF_DIR="$(mktemp -d)"
git clone "$APP_REPO_URL" "$PROOF_DIR/app"
cargo check --locked --manifest-path "$PROOF_DIR/app/Cargo.toml"
cargo test --locked --manifest-path "$PROOF_DIR/app/Cargo.toml"
```

For repository scripts, derive paths from the script location instead of assuming the current directory:

```sh
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
cargo check --locked --manifest-path "$REPO_ROOT/apps/my-app/Cargo.toml"
```

For local MPC app paths:

```sh
cargo run
```

Framework validation:

```sh
cargo test -p stoffel-rust-sdk
cargo run -p stoffel-rust-sdk --example quickstart
cargo run -p stoffel-rust-sdk --example local_mpc_client_input
```

## Common pitfalls

- Do not use path dependencies as the default after crates.io publication.
- Do not accept `git = "...", branch = "main"`; use the official URL and a full `rev`.
- Do not omit a generated app's `Cargo.lock` or silently drop `--locked` in CI.
- Do not treat a successful build inside the framework checkout as portability proof; workspace inheritance and nearby paths can hide leaks.
- Do not simulate protocol behavior in app code; use SDK/runtime execution paths.
- Do not present `.execute_local().await?` as a production deployment path.
- Do not compile `.stfl` source dynamically inside production clients; load pinned bytecode and generated metadata.
- Do not set an explicit backend that conflicts with bytecode metadata. Prefer generated manifests for ClientStore programs.
- For `ClientStore` apps, validate client input shapes before network submission.
- Do not use `stoffel-rust-sdk` as the binding generator build-dependency. Use the matching public `stoffel-bindgen` crate under `[build-dependencies]` as shown in the typed-bindings playbook.

## Next playbooks

- [Stoffel Typed Client IO Bindings](/developer-skills/stoffel-typed-client-io-bindings)
- [Stoffel Local MPC Dev Loop](/developer-skills/stoffel-local-mpc-dev-loop)
- [Stoffel App Network and Off-Chain Integration](/developer-skills/stoffel-app-network-and-offchain-integration)
- [Stoffel Deployment Runbook](/developer-skills/stoffel-deployment-runbook)

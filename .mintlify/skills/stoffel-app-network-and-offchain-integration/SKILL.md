---
name: stoffel-app-network-and-offchain-integration
description: Move from local bytecode to client/server builders, network config, and off-chain coordinator integration.
license: MIT
compatibility: Requires access to the Stoffel CLI/SDK docs and current app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-app-network-and-offchain-integration
  source: Stoffel App Developer Skills
---

# Stoffel App Network and Off-Chain Integration

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Package assumption: the app-facing crates from `StoffelVM` are expected to be published to crates.io. Prefer public package/install snippets when available. Use local path dependencies only for temporary WIP testing before publication or when testing unreleased framework changes.

## Use when

Use this playbook when an app moves beyond local runs and needs client/server builders, network config, off-chain coordinator integration, or typed ClientStore IO against real nodes.

## Goal

Guide advanced app developers from local bytecode to app-level network/off-chain integration using public SDK builders, while staying conservative about WIP lower-layer behavior.

## Current source of truth

- `StoffelVM/crates/stoffel-rust-sdk/README.md`
- `StoffelVM/crates/stoffel-rust-sdk/src/runtime.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/config.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/client.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/server.rs`
- `StoffelVM/crates/stoffel-rust-sdk/src/coordinator/offchain.rs`
- `StoffelVM/crates/stoffel-rust-sdk/examples/network_config.rs`
- `StoffelVM/crates/stoffel-rust-sdk/examples/client_server.rs`

## Preconditions

Before network integration, verify local behavior:

```sh
stoffel status --verbose
stoffel check
stoffel build --program-info
stoffel run --timeout-secs 180 <inputs or documented run-args>
```

If the app uses typed client IO, generate bindings from the exact bytecode first. See Stoffel Typed Client IO Bindings.

## Runtime builders

The SDK runtime exposes app-level builders:

```rust
let runtime = stoffel::Stoffel::load_file("program.stflb")?.build()?;

let client = runtime.client();
let server0 = runtime.server(0);
let deployment_client = runtime.client_for_deployment(&deployment);
let server_for_config = runtime.server_for_config(&config);
let servers = runtime.servers_for_deployment(&deployment);
```

For ClientStore apps:

```rust
let client_config = runtime.offchain_client_config(0)?;
```

Callers still provide coordinator address, node RPC addresses, timestamp, and client identity material explicitly.

## Network config concepts

App-level network config must align on:

- party id
- bind addresses and server addresses
- expected parties
- expected clients
- threshold
- backend and curve
- preprocessing sizes when required by the selected backend
- deployment-level mapping of party configs
- client slot and ClientStore IO shape

Use SDK builders so validation fails early:

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
```

## Off-chain ClientStore flow

1. Compile/build app bytecode.
2. Run local MPC with the same ClientStore inputs and expected output clients.
3. Generate typed bindings from that bytecode.
4. Build runtime from bytecode and generated manifest.
5. Derive off-chain client config for a client slot.
6. Attach coordinator address, node endpoints/RPC addresses, timestamp, and client identity material.
7. Run or submit typed client inputs.
8. Validate typed outputs and consensus/order evidence where applicable.

## CLI network execution

The CLI can execute against a network config:

```sh
stoffel run target/debug/app.stflb --network --config path/to/network-client.toml --client-id 0
```

Important: `--config` is network/off-chain client config, not app `Stoffel.toml`.

## Validation / done criteria

- Local smoke test passes first.
- Network config validates before starting servers/clients.
- Client IO metadata matches generated bindings.
- Real client/server run returns expected output or a concrete error with logs.
- Any WIP coordinator/network branch assumptions are labeled as WIP, not production deployment docs.

Framework WIP validation:

```sh
cargo test -p stoffel-rust-sdk
cargo run -p stoffel-rust-sdk --example network_config
cargo run -p stoffel-rust-sdk --example client_server
```

## Common pitfalls

- `stoffel run --config` is network/off-chain config, not project `Stoffel.toml`.
- Do not duplicate lower-level networking/protocol logic in app code.
- Do not bypass typed IO validation for ClientStore apps.
- Keep on-chain coordinator paths marked advanced until public docs and stable APIs exist.
- Do not present WIP coordinator/network branch assumptions as production deployment docs.
- Do not move to network debugging until the local loop has produced a real passing or failing run.

---
name: stoffel-app-network-and-offchain-integration
description: Move from local bytecode to client/server builders, network config, and off-chain coordinator integration.
license: MIT
compatibility: Requires access to the current Stoffel CLI/SDK docs and app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-app-network-and-offchain-integration
  source: Stoffel App Developer Skills
---

# Stoffel App Network and Off-Chain Integration

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Dependency assumption: use the current public install snippets from these docs. When developing against a local checkout, make that source-based workflow explicit.

## Use when

Use this playbook when an app moves beyond local runs and needs client/server builders, network config, off-chain coordinator integration, or typed ClientStore IO against real nodes.

## Goal

Guide advanced app developers from local bytecode to app-level network/off-chain integration using public SDK builders, while labeling lower-layer behavior with the current component status.

For client-owned private input, the participant-owned process is the Stoffel MPC client. It submits directly to the separately deployed MPC service. The application control plane may issue public session configuration and receive non-sensitive receipts or explicitly authorized opened aggregates, but it must not receive or persist participant plaintext.

## Separate the application roles

Do not combine these roles into one `client/app` layer:

| Role | Responsibility | Plaintext boundary |
| --- | --- | --- |
| Application control plane | Public metadata, authentication, session lifecycle, client-slot/capability assignment, network discovery, non-sensitive receipts, authorized aggregates | Must not receive participant private input |
| Participant MPC client | Loads pinned bindings/config, validates its owner's input, submits its assigned slot, decodes authorized output | May see only its owner's plaintext |
| MPC service plane | Separately deployed coordinator and long-running parties | Receives client-protocol material according to the deployment, not application-service plaintext |
| Output recipient | Participant client or application service named by the privacy worksheet | Receives only explicitly authorized output |

A backend gateway that accepts raw input is a distinct, weaker trust model. Name it and require explicit approval; do not introduce it to work around missing participant-runtime support.

## Current source of truth

- `crates/stoffel-rust-sdk/README.md`
- `crates/stoffel-rust-sdk/src/runtime.rs`
- `crates/stoffel-rust-sdk/src/config.rs`
- `crates/stoffel-rust-sdk/src/client.rs`
- `crates/stoffel-rust-sdk/src/server.rs`
- `crates/stoffel-rust-sdk/src/coordinator/offchain.rs`
- `crates/stoffel-rust-sdk/examples/network_config.rs`
- `crates/stoffel-rust-sdk/examples/client_server.rs`

## Preconditions

Before network integration, complete the trust-boundary worksheet in [Stoffel Full App Golden Path](/developer-skills/stoffel-full-app-golden-path). Identify the participant runtime, the process that executes client submission, components forbidden from plaintext, the control-plane persistence allowlist, and output recipients.

Then verify local program behavior:

```sh
stoffel status --verbose
stoffel check
stoffel build --program-info
stoffel run --timeout-secs 180 <inputs or documented run-args>
```

If the app uses typed client IO, generate bindings from the exact bytecode first. See [Stoffel Typed Client IO Bindings](/developer-skills/stoffel-typed-client-io-bindings).

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
7. Configure the separately deployed MPC service layer with the same bytecode, topology, backend, and client/output slots.
8. Have each participant-owned client submit its own typed input directly to that deployment.
9. Reconcile only non-sensitive submission status with the application control plane.
10. Deliver typed outputs only to recipients authorized by the privacy worksheet.
11. Validate typed outputs and consensus/order evidence where applicable.

The SDK can validate and carry the app-level config, but live network deployment also needs operator-owned process supervision, identity files, node RPC reachability, and persistence/state decisions. Use [Stoffel Deployment Runbook](/developer-skills/stoffel-deployment-runbook) for that handoff.

## Control-plane bootstrap and receipts

A control plane may return public session configuration such as:

```json
{
  "sessionId": "session_123",
  "clientSlot": 1,
  "programHash": "sha256:...",
  "inputSchemaId": "prediction-v1",
  "coordinatorEndpoint": "https://coordinator.example.com",
  "nodeRpcEndpoints": ["https://node-0.example.com"],
  "deploymentEpoch": 42,
  "submissionCapability": "short-lived-signed-token"
}
```

A non-sensitive receipt may contain:

```json
{
  "sessionId": "session_123",
  "clientSlot": 1,
  "submissionId": "sub_456",
  "status": "accepted",
  "receivedAt": "..."
}
```

Do not place participant predictions, typed private inputs, reversible encodings, generic private payload blobs, secret-sharing randomness, or participant shares in control-plane APIs, persistence, logs, queues, analytics, or receipts.

## Participant runtime capability gate

Resolve this before implementation:

| Participant runtime | Required decision |
| --- | --- |
| Native or Rust client, including participant-side Tauri Rust | Use direct participant-to-MPC submission when supported by the current SDK |
| Browser/WASM with a supported Stoffel client package | Submit directly from the participant client |
| Browser/WASM without direct support | Stop at the capability gap or use an explicitly participant-controlled sidecar; do not proxy plaintext through the backend |
| Backend gateway | Degraded trust: the gateway sees raw input and requires explicit approval |
| Local CLI or fixture harness | Development evidence only; not production private-data-plane evidence |

## CLI network execution

The CLI can execute against a network config:

```sh
stoffel run target/debug/app.stflb --network --config path/to/network-client.toml --client-id 0
```

Important: `--config` is network/off-chain client config, not app `Stoffel.toml`.

## Validation / done criteria

- Local smoke test passes first.
- Bytecode hash and generated bindings are recorded together.
- Coordinator address, node mesh addresses, node RPC addresses, identity material, and expected client certificates are explicitly configured or listed as operator handoff fields.
- Network config validates before starting servers/clients.
- Client IO metadata matches generated bindings.
- Real participant-client/network run returns expected output or a concrete error with logs.
- Control-plane schemas, persistence, logs, and receipts contain no participant plaintext.
- A plaintext canary test confirms private input bypasses application-service requests, storage, queues, caches, traces, analytics, and crash reports.
- The participant runtime has verified direct client-protocol support or an explicit capability blocker/participant-controlled sidecar decision.
- Every output recipient matches the privacy worksheet.
- Any coordinator/network assumptions are labeled with current component status and paired with deployment validation guidance.

Framework validation:

```sh
cargo test -p stoffel-rust-sdk
cargo run -p stoffel-rust-sdk --example network_config
cargo run -p stoffel-rust-sdk --example client_server
```

## Common pitfalls

- `stoffel run --config` is network/off-chain config, not project `Stoffel.toml`.
- Do not duplicate lower-level networking/protocol logic in app code.
- Do not treat participant clients and the application control plane as one trust role.
- Do not add plaintext private fields to control-plane endpoints or persistence.
- Do not put `.with_client_input(...)` or `.execute_local()` in a production application-service path.
- Do not silently replace missing browser/client support with a plaintext backend gateway.
- Do not bypass typed IO validation for ClientStore apps.
- Keep on-chain coordinator paths marked advanced until public docs and stable APIs exist.
- Present coordinator/network assumptions with explicit current status and deployment validation guidance.
- Do not move to network debugging until the local loop has produced a real passing or failing run.
- Do not hide missing production process startup behind local SDK examples; record the lower-layer service command or mark it as an operator handoff.

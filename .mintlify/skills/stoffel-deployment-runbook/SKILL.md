---
name: stoffel-deployment-runbook
description: Prepare and verify a production-shaped Stoffel deployment with compiled bytecode, typed client IO, node topology, coordinator settings, identity material, and operational checks.
license: MIT
compatibility: Requires access to the current Stoffel CLI/SDK docs and app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-deployment-runbook
  source: Stoffel App Developer Skills
---

# Stoffel Deployment Runbook

> Scope: app/operator playbook for moving a verified Stoffel app from local MPC into a production-shaped network deployment. This is not a maintainer guide for protocol internals.
>
> Dependency assumption: use public CLI/SDK surfaces first. If a current SDK wrapper does not start the lower-layer service directly, state the lower-layer handoff instead of pretending local MPC is deployment.

## Use when

Use this playbook when a Stoffel app already passes local CLI/SDK smoke tests and now needs deployable artifacts, node/client topology, off-chain coordinator config, or an operator runbook.

## Goal

Make deployment explicit enough that an agent does not guess hidden topology, identity, bytecode, or client-slot details. A deployment is complete only when a client can submit typed inputs to the intended network and receive the authorized output, or when the remaining lower-layer blocker is recorded with logs.

## Deployment model

Production-shaped Stoffel apps have three layers:

1. Build artifacts: `.stflb` bytecode, generated typed bindings, program manifest, and app release metadata.
2. MPC service layer: coordinator plus long-running MPC parties/nodes with stable network addresses and identity material.
3. Client/app layer: backend service, CLI, native app, or future browser/WASM client that loads deployment config, selects a client slot, submits inputs, and reads typed outputs.

Do not use `.execute_local().await?` as the deployment model. It is the local development analogue that spawns several MPC nodes/processes on one machine.

## Portability and provenance preflight

Label each command and artifact observation with one execution context: **app checkout**, **framework checkout**, **deployment host**, **container**, or **CI**. A host command does not prove what a container sees, and a framework workspace command does not prove that an external app can consume the public packages.

Before building the release bundle, record:

- app repository URL, commit, and clean/dirty state;
- framework repository URL, commit, and clean/dirty state when a framework checkout is intentionally involved;
- CLI installation source, resolved executable path, and reported version/build identity when available;
- SDK source as a public package version or git URL plus revision; record any intentional path source explicitly;
- committed lockfile path and hash, or the reason a lockfile does not apply;
- bytecode, generated binding, and program/deployment manifest hashes;
- immutable container image digest for every applicable build and runtime image.

The release candidate must pass in a **clean external app checkout** outside the framework repository. Resolve only documented public dependencies: no undeclared path dependencies, workspace inheritance, unpublished local packages, framework source mounts, or dirty generated files. Run a minimal public dependency consumer through check, build, binding generation, and its client-facing smoke path. Record its repository URL/commit, clean state, lockfile, dependency resolution, commands, and outputs. A framework-checkout test does not substitute for this proof. If the proof is unavailable, label the candidate **not clean-room tested** and do not present it as portable.

## Deployment inputs to collect

Before editing deployment code, fill this table:

| Field | Value |
| --- | --- |
| Bytecode path | `dist/program.stflb` |
| Program hash / build ID |  |
| Backend | `honeybadger` or `avss:<curve>` |
| Parties |  |
| Threshold |  |
| Expected input clients |  |
| Expected output clients |  |
| Coordinator host/port |  |
| Party mesh addresses |  |
| Node RPC addresses |  |
| Client slots |  |
| Party identity files |  |
| Client identity files |  |
| Timestamp / deployment epoch |  |
| Preprocessing sizes |  |
| Persistence/state volume |  |
| Health/log endpoints |  |
| App repo URL / commit / clean state |  |
| Framework repo URL / commit / clean state, if used |  |
| CLI source / resolved path |  |
| SDK source |  |
| Lockfile path / hash |  |
| Bytecode / binding / manifest hashes |  |
| Build and runtime image digests, if used |  |
| Execution contexts used | app checkout / framework checkout / deployment host / container / CI |
| Clean external consumer proof | pass / fail / skipped with reason |

If any field is unknown, stop and discover it from source, generated metadata, deployment config, or operator input. Do not invent it.

## Artifact build step

Build artifacts before deploying services:

```sh
stoffel status --verbose
stoffel check
stoffel build --program-info
```

For Rust app wrappers:

```sh
cargo check --locked
cargo test --locked
```

Expected artifacts:

```text
dist/program.stflb
dist/stoffel_bindings.rs or generated bindings in OUT_DIR
release manifest with backend, parties, threshold, client slots, and output slots
```

Record all bundle member hashes in the deployment notes. Make the release bundle immutable after this point. Production services and clients must load this unchanged bytecode, bindings, manifest, and config set; do not rebuild, regenerate, or dynamically compile `.stfl` independently on deployment hosts. Recheck hashes at distribution, service startup, and client execution.

## Local gate before network work

Run the same program shape locally:

```sh
stoffel run --timeout-secs 180 <documented inputs or # run-args>
```

For Rust SDK local smoke:

```sh
cargo run --locked --bin <local-smoke-or-demo>
```

The local gate must cover:

- every ClientStore input slot used by deployment;
- expected output clients;
- backend/topology selection when configurable;
- typed output decoding when generated bindings are used.

## Network config plan

Use SDK builders for topology validation when possible:

```rust
let deployment = NetworkDeployment::builder([
    "node-0.internal:19200",
    "node-1.internal:19201",
    "node-2.internal:19202",
    "node-3.internal:19203",
    "node-4.internal:19204",
])
.expected_clients(2)
.threshold(1)
.honeybadger()
.consensus_timeout(std::time::Duration::from_secs(60))
.preprocessing(1000, 500)
.build()?;

let paths = deployment.save_toml_files("deploy/network")?;
```

Each party config must agree on:

- party id;
- bind address;
- peer addresses;
- expected parties;
- expected clients;
- threshold;
- backend/curve;
- preprocessing sizes;
- coordinator/off-chain settings when using ClientStore IO.

## Server/node handoff

A node service needs:

- the exact `.stflb` bytecode;
- the party’s network config;
- coordinator address if using off-chain ClientStore IO;
- node RPC bind address;
- party certificate/key material;
- expected client certificates;
- persistent state location when the backend/workflow stores shares or commitments;
- process supervisor and logs.

SDK server builders validate app-level config:

```rust
let app_root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
let runtime = Stoffel::load_file(app_root.join("dist/program.stflb"))?
    .parties(5)
    .threshold(1)
    .honeybadger()
    .build()?;

let servers = runtime.servers_for_deployment(&deployment);
let server0 = servers[0].clone().build()?;
```

Current SDK server builders capture program/config/health metadata; live process startup may delegate to lower-layer networking/VM integration. If the selected SDK version does not expose a single production server start command, write the lower-layer command or service wrapper explicitly and mark it as an operator handoff, not as completed deployment.

### Container and host safeguards

- Pin every image by digest and record that digest with the node/client result.
- Record each host-to-container mount. Mount the immutable release bundle read-only where possible, keep state and identity mounts separate, and verify bundle hashes inside every runtime container.
- Never mount a framework checkout, developer `target/`, or unpublished package cache to make a release work. Such a run is **not clean-room tested**.
- Distinguish bind addresses from advertised/reachable addresses. `127.0.0.1` and `localhost` refer to the current network namespace and normally cannot identify a service across host/container boundaries.
- Publish only required ports, and test coordinator, mesh, RPC, and client reachability from the actual source container/host. Record DNS resolution and the address used, not only a host-side health result.

## Client/app integration

Client software should load deployment config and submit typed inputs:

```rust
let app_root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
let runtime = Stoffel::load_file(app_root.join("dist/program.stflb"))?
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

let client = runtime
    .client_for_deployment(&deployment)
    .offchain_io(offchain)
    .client_id(0)
    .connect()
    .await?;

let outputs = client
    .run_typed::<Client0Inputs, Client0Outputs>(Client0Inputs { input_0: 42 })
    .await?;
```

If the app uses a backend gateway, state the security boundary: the gateway sees the user’s raw input before secret sharing. If raw input must stay out of the gateway, the app needs a client-side sharing package or another submission path; do not hide that gap.

## Operational checklist

Before calling deployment done:

- Bytecode and bindings come from the same build.
- All nodes run the same bytecode hash and compatible configs.
- The coordinator address is reachable from every node and client.
- Node mesh ports and node RPC ports are reachable according to the topology.
- Party and client identity files are present, readable by the process, and not committed.
- Client slots and output slots match the generated manifest.
- Preprocessing capacity covers the expected workload shape.
- Logs redact private inputs, identity material, tokens, and certificates.
- Restart behavior is documented for coordinator, nodes, and client gateway.
- Rollback means reverting bytecode, bindings, config, and app client code together.
- Repository, CLI, SDK, lockfile, artifact, and image provenance is recorded for each labeled execution context.
- The external clean-checkout/public dependency consumer proof passed.
- Every deployment host/container verified the unchanged release bundle hashes before startup.
- The real service processes started and an actual SDK client traversed the intended coordinator/node service path and decoded the authorized typed output.

Builder construction, config serialization, `.execute_local()`, `execute_local`, or any other local-only executor is not deployment completion. If no live service path is available, report the deployment as blocked or incomplete with the exact handoff and logs. Do not rebuild the bundle merely to make the client smoke pass.

## Verification commands

Use the commands that exist for the app. A typical ladder is:

```sh
stoffel check
stoffel build --program-info
cargo check --locked
cargo test --locked
cargo run --locked --bin build-program
cargo run --locked --bin validate-network-config
cargo run --locked --bin client-smoke -- --client-slot 0
```

For external services, also record:

```sh
curl -f http://<service>/health
```

and the process supervisor status/log command used by the deployment target.

## CI/release gates

Use separately visible gates for provenance capture, clean app build, public dependency consumer proof, lockfile/dependency inspection, bytecode/binding/manifest hash agreement, image digest capture, deployment config validation, service startup/health, cross-namespace reachability, and the real SDK client/service smoke. CI must fail on a dirty checkout, unexpected local/path/patched dependency, lockfile drift, mutable-only image identity, bundle mutation, or failed service/client flow.

Never omit a gate from the report. Mark each one `passed`, `failed`, or `skipped`. For a skip, record the exact reason, execution context, owner/handoff, and impact; for example, **not clean-room tested**, **container provenance unknown**, or **deployment unverified**. A skipped completion gate cannot produce a successful deployment status.

## Failure report shape

When deployment fails, capture:

- bytecode hash;
- branch/commit;
- party id or client slot;
- command run;
- redacted config path;
- first failing log line;
- whether local MPC passed;
- whether typed bindings matched;
- whether the failure is build, config validation, network reachability, identity, coordinator, protocol, or output decoding;
- labeled execution context and working directory;
- exact command, exit status, first actionable error, and unabridged log location;
- app/framework repository URLs, commits, and dirty state;
- CLI source, SDK source, lockfile hash, bundle member hashes, and applicable image digest;
- mount map and bind/advertised addresses when containers are involved;
- every skipped check and why it was skipped.

## Common pitfalls

- Calling local MPC deployment because it returned the right answer on one machine.
- Letting each node compile source independently instead of distributing pinned bytecode.
- Running clients against bindings generated from stale bytecode.
- Forgetting node RPC addresses when using off-chain ClientStore IO.
- Committing client or party keys.
- Treating backend/curve changes as config-only changes without rebuilding and revalidating artifacts.
- Hiding a missing production server wrapper behind local SDK examples.

## Next playbooks

- [Stoffel Full App Golden Path](/developer-skills/stoffel-full-app-golden-path)
- [Stoffel App Network and Off-Chain Integration](/developer-skills/stoffel-app-network-and-offchain-integration)
- [Stoffel Rust App SDK](/developer-skills/stoffel-rust-app-sdk)
- [Stoffel App Troubleshooting](/developer-skills/stoffel-app-troubleshooting)

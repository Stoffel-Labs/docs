---
name: stoffel
description: Build applications with Stoffel, a privacy-first MPC framework. Use these skills to create apps, write Stoffel-Lang, run local MPC, use the Rust SDK, generate typed client IO bindings, and troubleshoot app workflows.
license: MIT
compatibility: Requires Stoffel docs, Rust stable/Cargo for CLI and Rust SDK workflows, and a local `stoffel-run` binary for local MPC execution.
metadata:
  author: Stoffel Labs
  version: "1.0"
---

# Stoffel Developer Skills

Stoffel exposes multiple focused skills under `.mintlify/skills/` and the `/.well-known/agent-skills/` discovery endpoint. Use the most specific skill for the task:

- `stoffel-app-getting-started`: Install the Stoffel tooling, create a new app, run first local smoke tests, and choose the right development path.
- `stoffel-cli-app-workflow`: Use the stoffel CLI to init, check, build, compile, run, test, inspect, and troubleshoot Stoffel apps.
- `stoffel-lang-app-programming`: Write .stfl application logic using supported Stoffel-Lang syntax, types, builtins, and example patterns.
- `stoffel-secret-mpc-programming`: Build MPC apps with secret types, Share, ClientStore, Mpc, MpcOutput, and runnable private-input examples.
- `stoffel-rust-app-sdk`: Embed Stoffel in Rust apps using the SDK for compilation, bytecode loading, local execution, clients, and servers.
- `stoffel-typed-client-io-bindings`: Generate and use Rust typed client input/output bindings from exact Stoffel bytecode manifests.
- `stoffel-local-mpc-dev-loop`: Run local MPC smoke tests, ClientStore input flows, hot reload, and SDK local coordinator-backed execution.
- `stoffel-app-network-and-offchain-integration`: Move from local bytecode to client/server builders, network config, and off-chain coordinator integration.
- `stoffel-app-troubleshooting`: Diagnose app-level init, check, build, run, local MPC, binding, SDK, and network failures with evidence.

For human-readable versions, start at `/developer-skills/overview`.

---
name: stoffel
description: Build applications with Stoffel, a privacy-first MPC framework. Use these skills to create apps, write StoffelLang, run local MPC, use the Rust SDK, generate typed client IO bindings, prepare deployment-shaped network handoffs, and troubleshoot app workflows.
license: MIT
compatibility: Requires Stoffel docs and Rust stable/Cargo for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
---

# Stoffel Developer Skills

Stoffel exposes multiple focused skills under `.mintlify/skills/` and the `/.well-known/agent-skills/` discovery endpoint. Use the most specific skill for the task:

- `stoffel-app-getting-started`: Install the Stoffel tooling, create a new app, run first local smoke tests, and choose the right development path.
- `stoffel-cli-app-workflow`: Use the stoffel CLI to init, check, build, compile, run, test, inspect, and troubleshoot Stoffel apps.
- `stoffel-full-app-golden-path`: Build a complete app from privacy boundary through StoffelLang, Rust SDK integration, local MPC validation, typed bindings, and deployment handoff.
- `stoffel-lang-app-programming`: Write .stfl application logic using supported Stoffel-Lang syntax, types, builtins, and example patterns.
- `stoffel-secret-mpc-programming`: Build MPC apps with secret types, Share, ClientStore, Mpc, MpcOutput, and runnable private-input examples.
- `stoffel-rust-app-sdk`: Embed Stoffel in Rust apps using the SDK for compilation, bytecode loading, local execution, clients, and servers.
- `stoffel-typed-client-io-bindings`: Generate and use Rust typed client input/output bindings from exact Stoffel bytecode manifests.
- `stoffel-local-mpc-dev-loop`: Run local MPC smoke tests, ClientStore input flows, hot reload, and SDK local coordinator-backed execution.
- `stoffel-app-network-and-offchain-integration`: Move from local bytecode to client/server builders, network config, and off-chain coordinator integration.
- `stoffel-deployment-runbook`: Prepare production-shaped artifacts, topology, coordinator settings, identity material, client config, and operational verification.
- `stoffel-app-troubleshooting`: Diagnose app-level init, check, build, run, local MPC, binding, SDK, and network failures with evidence.
- `stoffel-ai-agent-implementation`: Give AI coding agents backend, input/output, validation, and cost-model context before they write Stoffel code.

For human-readable versions, start at `/developer-skills/overview`.

## Mandatory portability contract

Apply this contract to every app task unless the user explicitly requests Stoffel framework development:

1. Discover and confirm the project root from the current working directory and repository markers such as `Stoffel.toml`, `Cargo.toml`, or `.git`. Never invent or require a machine-specific path such as `/workspace/...`.
2. Resolve Stoffel and related project dependencies from public, reproducible sources in this order: the current crates.io release, an official GitHub tag or release, then a full immutable commit SHA in the official GitHub repository.
3. Never use a floating branch, and never make a local path, sibling checkout, or other external filesystem checkout a requirement for the default app workflow.
4. Use a local Stoffel checkout only when the user explicitly asks to develop the framework itself. Label that route **nonportable** and keep it separate from the default public-dependency instructions.
5. If no suitable public dependency is available, stop and report the missing dependency and attempted public sources. Do not silently substitute a local checkout or fabricate a path.

Keep skill guidance version-agnostic. Put concrete dependency versions in the installation documentation or the app's dependency manifest, not in skill text.

## Agent bootstrap

Install the `stoffel` CLI, these skills, and live docs access:

```sh
curl -fsSL https://get.stoffelmpc.com | sh
export PATH="$HOME/.local/bin:$PATH"
stoffel --version
stoffel --help
npx skills add https://docs.stoffelmpc.com --all
npx add-mcp --name stoffel-docs --transport http https://docs.stoffelmpc.com/mcp
stoffel init hello-mpc
cd hello-mpc
stoffel status --verbose
stoffel check
stoffel build
```

For runnable app tasks, report real output from `stoffel status --verbose`, `stoffel check`, `stoffel build`, a local MPC run, and any relevant Cargo command before claiming completion. Do not claim completion until portability validation has passed in a clean environment without an external Stoffel checkout.

Discovery endpoints:

- `https://docs.stoffelmpc.com/.well-known/agent-skills/index.json`
- `https://docs.stoffelmpc.com/.well-known/skills/index.json`
- `https://docs.stoffelmpc.com/.well-known/mcp`
- `https://docs.stoffelmpc.com/.well-known/mcp/server-card.json`

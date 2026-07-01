---
name: stoffel-ai-agent-implementation
description: Give AI coding agents the context they need to build and validate Stoffel applications correctly.
license: MIT
compatibility: Requires access to the Stoffel CLI/SDK docs and 0.1.0 app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-ai-agent-implementation
  source: Stoffel App Developer Skills
---

# Stoffel AI Agent Implementation

Use this skill when asking an AI coding agent to build, modify, deploy, or debug a Stoffel application. The goal is to give the agent enough context to choose the right MPC backend, model secret inputs correctly, and validate the smallest working program before expanding the app.

## Give the agent Stoffel docs access

Before a large implementation task, install the Stoffel skills and connect the live docs MCP server so the agent can use current docs instead of training-data guesses.

Install the skills:

```sh
npx skills add https://docs.stoffelmpc.com
```

List the published skills first if you need to choose a narrower playbook:

```sh
npx skills add https://docs.stoffelmpc.com --list
```

Connect the Mintlify-hosted search MCP server:

```sh
npx add-mcp --name stoffel-docs --transport http https://docs.stoffelmpc.com/mcp
```

For Claude Code directly:

```sh
claude mcp add --transport http stoffel-docs https://docs.stoffelmpc.com/mcp
```

Programmatic discovery endpoints:

- `https://docs.stoffelmpc.com/.well-known/agent-skills/index.json`
- `https://docs.stoffelmpc.com/.well-known/mcp`
- `https://docs.stoffelmpc.com/.well-known/mcp/server-card.json`

## Start with the implementation boundary

Before asking an agent to write code, describe the boundary the Stoffel program must implement:

1. Which values are secret.
2. Which values are public.
3. Who supplies each input.
4. Who receives each output.
5. Whether each output is an opened value, client-output share, public commitment, curve-encoded value, or signature-related artifact.
6. Which backend is selected and why.
7. Which command proves the program is valid.
8. Which command proves local MPC works.
9. Which artifacts and configs are required before deployment.

For source snippets, the validation command is usually:

```bash
stoffel check path/to/program.stfl
```

For docs changes, also run:

```bash
npx mintlify validate
npx mintlify broken-links
```

## Backend selection context

Give the agent the backend decision in terms of value representation and output boundary.

Use HoneyBadgerMPC when:

- the program computes over secret integers, fixed-point values, or field-compatible shares;
- the main cost questions are multiplication count, multiplication depth, comparisons, and reveal boundaries;
- public parameters can stay public while private inputs remain ordinary MPC shares;
- the outside system consumes an opened result or client-output shares from private computation.

Use AVSS when:

- the program needs public commitments to secret shares;
- the backend must use a curve that matches an external verifier or protocol;
- public transcript bytes must become curve-field challenges;
- the outside system consumes a commitment, curve-encoded value, opened scalar response, or signature-related artifact.

If the task is ordinary private arithmetic over application values, start with HoneyBadgerMPC. Use AVSS only when the protocol needs committed scalar shares, curve compatibility, or threshold-cryptography artifacts.

## Prompt template

```text
Build the smallest StoffelLang program for this task before expanding it.

Secret values:
- ...

Public values:
- ...

Input owners:
- client 0 supplies ...
- client 1 supplies ...

Output boundary:
- opened value / client-output share / public commitment / curve-encoded artifact / signature-related artifact

Backend:
- honeybadger or avss:<curve>
- reason for choosing it

Cost and safety constraints:
- keep public constants, transcript bytes, hashes, and encodings public until a secret operation needs them
- avoid secret × secret multiplication unless required
- use public weights/constants when they are not private inputs
- minimize openings and reveal only the intended output boundary
- for AVSS signing flows, never persist or reuse per-signature nonces unless the protocol explicitly requires and protects that state

Validation:
- run `stoffel check ...`
- run `stoffel build --program-info`
- run a local MPC smoke with documented inputs
- if deployment is requested, produce bytecode, bindings, topology, coordinator/client config, and operator handoff fields
- if editing docs, run `npx mintlify validate` and `npx mintlify broken-links`
```

## HoneyBadgerMPC agent guidance

Ask the agent to inspect circuit shape before optimizing code:

- Count secret × secret multiplications.
- Separate multiplication count from multiplication depth.
- Keep public weights, thresholds, normalization factors, and lookup tables public when possible.
- Treat comparisons, bit decomposition, and nonlinear functions as expensive until measured.
- Use `MpcOutput` when a client should receive result shares instead of opening the result to the host application.
- Size preprocessing for the largest expected input shape if the program runs on a network deployment.

Useful APIs and concepts:

- `ClientStore.get_number_clients()`
- `ClientStore.take_share(...)`
- `ClientStore.take_share_fixed(...)`
- `Mpc.has_capability("client-output")`
- `MpcOutput.send_to_client(...)`
- `Share.add`, `Share.mul`, `Share.mul_scalar`
- opened values via `.reveal()`, `Share.open(...)`, or `open_fixed()` where appropriate

## AVSS agent guidance

Ask the agent to keep the cryptographic transcript explicit:

- Choose the curve based on the external verifier or protocol.
- Keep transcript bytes public until they become a scalar challenge with `Crypto.hash_to_field(..., Mpc.curve())`.
- Use `get_commitment(0)` when the outside system needs a public commitment or public key point.
- Persist long-lived key shares with `LocalStorage` when the workflow requires stable key material.
- Do not persist or reuse per-signature nonces unless the protocol explicitly requires and protects that state.
- Minimize openings; open scalar responses only when the protocol boundary requires it.

Useful APIs and concepts:

- `Share.random()`
- `LocalStorage.exists(...)`
- `LocalStorage.store(...)`
- `LocalStorage.load(...)`
- `LocalStorage.load_share(...)`
- `secret_key.get_commitment(0)`
- `Mpc.curve()`
- `Crypto.hash_to_field(...)`
- `Crypto.point_to_sec1(...)`
- `MpcOutput.send_to_client(...)`

## Common corrections to give the agent

- Do not use AVSS for generic private arithmetic unless the task needs commitments or curve-compatible artifacts.
- Do not reveal intermediate secret values just to make the program easier to write.
- Do not turn public transcript material into secret shares earlier than necessary.
- Do not assume a curve selector applies to HoneyBadgerMPC.
- Do not stop after writing code; run the relevant validation command and report the real output.

## See also

- [MPC Backends](/mpc-protocols/overview)
- [Performance and Circuit Shaping](/mpc-protocols/performance-and-circuit-shaping)
- [HoneyBadgerMPC](/mpc-protocols/honeybadger-mpc)
- [AVSS](/mpc-protocols/avss)
- [Stoffel Full App Golden Path](/developer-skills/stoffel-full-app-golden-path)
- [Stoffel Secret MPC Programming](/developer-skills/stoffel-secret-mpc-programming)
- [Stoffel Local MPC Dev Loop](/developer-skills/stoffel-local-mpc-dev-loop)
- [Stoffel Deployment Runbook](/developer-skills/stoffel-deployment-runbook)

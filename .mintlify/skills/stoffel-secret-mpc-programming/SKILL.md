---
name: stoffel-secret-mpc-programming
description: Build MPC apps with secret types, Share, ClientStore, Mpc, MpcOutput, and runnable private-input examples.
license: MIT
compatibility: Requires access to the current Stoffel CLI/SDK docs and app-facing Stoffel tooling. Rust stable and Cargo are required for CLI and Rust SDK workflows.
metadata:
  author: Stoffel Labs
  version: "1.0"
  docs-page: /developer-skills/stoffel-secret-mpc-programming
  source: Stoffel App Developer Skills
---

# Stoffel Secret MPC Programming

> Scope: AI-agent-agnostic playbook for building applications with the Stoffel framework. This is not a maintainer guide for compiler, VM, protocol, or release engineering work.
>
> Dependency assumption: use the current public install snippets from these docs. When developing against a local checkout, make that source-based workflow explicit.

## Use when

Use this playbook when an app handles private values, secret shares, client-provided inputs, MPC output delivery, protocol/runtime metadata, or secure algorithm examples.

## Goal

Help developers write MPC-oriented Stoffel apps using `secret` types, `Share.*`, `ClientStore.*`, `Mpc.*`, `MpcOutput.*`, and related builtins, while preserving runnable local examples.

## Current source of truth

- `crates/stoffel-lang/examples/README.md`
- `crates/stoffel-lang/examples/COVERAGE.md`
- `crates/stoffel-lang/examples/mpc_*`
- `crates/stoffel-lang/examples/bits/secret/*`
- `crates/stoffel-lang/examples/matrix/secret/*`
- `crates/stoffel-lang/examples/polynomials/secret/*`
- `crates/stoffel-lang/examples/number_theory/secret/*`
- `crates/stoffel-lang/examples/avss_*`
- `crates/stoffel-lang/examples/threshold_signatures/*`

## Minimal secret app

```stfl
def main(a: secret int64, b: secret int64) -> secret int64:
  return a + b
```

When run locally through the CLI/SDK, source/file programs returning a secret value may be wrapped/opened by the local execution path so app tests can assert clear outputs.

For client-owned private inputs, prefer `ClientStore`:

```stfl
# run-args: --client-input 0=40 --client-input 1=2 --expected-output-clients 2

def main() -> None:
  var a: secret int64 = ClientStore.take_share(0, 0)
  var b: secret int64 = ClientStore.take_share(1, 0)
  var sum: secret int64 = a + b
  MpcOutput.send_to_client(0, [sum])
  MpcOutput.send_to_client(1, [sum])
```

The first argument to `ClientStore.take_share(client_slot, input_index)` is the client slot. The second is that client's ordered input index. Repeating `--client-input 0=...` appends inputs for slot `0` in order.

## Secret values and shares

Common patterns:

```stfl
var x: secret int64 = Share.random()
var y = Share.from_clear_int(5, 1)
var sum: secret int64 = x + y
var product: secret int64 = x * y
var opened: int64 = sum.reveal()
```

Prefer `secret T` annotations when you know the share's scalar shape. The `secret` keyword belongs inside type annotations for parameters, return types, local variables, list elements, and object fields:

```stfl
def score(raw: secret int64, weight: int64) -> secret int64:
  var scaled: secret int64 = raw * weight
  return scaled + 10
```

Do not use `secret` as a declaration modifier before `def` or `var`. Use `var x: secret int64 = ...`, not `secret var x = ...`.

Use normal arithmetic operators (`+`, `-`, `*`, `/`) for secret values when the operation fits the value shape. Method/function forms such as `Share.add`, `Share.mul`, `.add_scalar`, and `.mul_scalar` remain useful when you want to call a specific builtin explicitly.

For fixed-point client inputs:

```stfl
var fixed: secret fix64 = ClientStore.take_share_fixed(0, 0)
```

For boolean circuits:

```stfl
def gate_and(a: secret bool, b: secret bool) -> secret bool:
  return a * b

def gate_not(a: secret bool) -> secret bool:
  return 1 - a

def gate_or(a: secret bool, b: secret bool) -> secret bool:
  var ab: secret bool = gate_and(a, b)
  return a + b - ab

def gate_xor(a: secret bool, b: secret bool) -> secret bool:
  var ab: secret bool = gate_and(a, b)
  return a + b - (ab * 2)
```

## Client input shares

Use `ClientStore` when the app receives private client inputs through the coordinator/client path:

```stfl
var value = ClientStore.take_share(0, 0)
var fixed = ClientStore.take_share_fixed(0, 1)
var n_clients: int64 = ClientStore.get_number_clients()
var n_input_clients: int64 = ClientStore.get_number_input_clients()
var n_output_clients: int64 = ClientStore.get_number_output_clients()
```

CLI flags:

```sh
stoffel run src/main.stfl \
  --client-input 0=42 --client-input 0=58 \
  --client-input 1=7 \
  --expected-output-clients 2
```

Input-file equivalents are documented in [Stoffel CLI App Workflow](/developer-skills/stoffel-cli-app-workflow).

## Client outputs

Send share outputs to clients when the runtime advertises that capability:

```stfl
if Mpc.has_capability("client-output"):
  MpcOutput.send_to_client(0, [result_share])
```

Many current examples now document `--expected-output-clients N` in a first-line `# run-args:` header. Preserve that flag in local runs; without it, output-capable client slots may not be declared in the local runtime.

## Runtime metadata

Useful app metadata:

- `Mpc.party_id()`
- `Mpc.n_parties()`
- `Mpc.threshold()`
- `Mpc.instance_id()`
- `Mpc.protocol_name()`
- `Mpc.curve()` / `Mpc.field()`
- `Mpc.is_ready()`
- `Mpc.has_capability(name)`
- `Mpc.capabilities()`
- `Mpc.rand()` / `Mpc.rand_int()`

## Example families to inspect

MPC primitive examples:

- `mpc_share_arithmetic`
- `mpc_boolean_circuit`
- `mpc_bitwise_share`
- `mpc_random_bit`
- `mpc_bit_decomposition`
- `mpc_secure_comparison`
- `mpc_select_minmax`
- `mpc_aes128_circuit`
- `mpc_client_private_score`
- `mpc_client_federated_average`
- `mpc_protocol_coordination`
- `mpc_share_toolkit`

Secure algorithm examples with recent client I/O headers:

- Comparison and bit algorithms: `mpc_range_check`, `mpc_clamp`, `mpc_compare_family`, `mpc_is_zero`, `mpc_popcount_secret`, `mpc_msb_log2`, `mpc_lowest_set_bit`, `mpc_parity`, `mpc_bit_reverse_rotate`, `mpc_sign_extend`.
- Oblivious data access/search: `mpc_oblivious_read`, `mpc_oblivious_write`, `mpc_mux_tree`, `mpc_linear_search`, `mpc_lookup_table`, `mpc_pattern_match`.
- Arithmetic/number theory: `mpc_secure_division`, `mpc_modulo_secret`, `mpc_mod_constant`, `mpc_gcd`, `mpc_lcm`, `mpc_reciprocal`, `mpc_sqrt`, `mpc_horner_eval`, `mpc_secret_base_power`, `mpc_secret_exponentiation`, `mpc_modexp`, `mpc_modinv`, `mpc_transcendental`.
- Sorting/ranking/arrays: `mpc_bitonic_sort`, `mpc_secure_shuffle`, `mpc_top_k`, `mpc_rank_order`.

Gallery examples:

- `bits/secret/*`: private bit/boolean circuits with `ClientStore` inputs.
- `matrix/secret/*`: private matrix/vector and fixed-point examples.
- `polynomials/secret/*`: polynomial, interpolation, coding, and private matching examples.
- `number_theory/secret/*`: private GCD, modular inverse, CRT, MAC, equality, and Diophantine examples.

Advanced protocol/crypto examples:

- `avss_share_auditor`
- `avss_certificate/*`
- `threshold_signatures/*`

## Validation / done criteria

For a secret app source change:

```sh
stoffel check path/to/main.stfl
stoffel build path/to/main.stfl
stoffel run path/to/main.stfl --timeout-secs 180 <documented run args>
```

For an example with a `# run-args:` header, use the exact flags from that header. Example:

```sh
stoffel run crates/stoffel-lang/examples/mpc_bitonic_sort/main.stfl \
  --client-input 0=7 --client-input 0=3 --client-input 0=5 --client-input 0=1 \
  --client-input 0=8 --client-input 0=2 --client-input 0=6 --client-input 0=4 \
  --expected-output-clients 1 \
  --timeout-secs 180
```

Framework validation:

```sh
cd /path/to/stoffel/crates/stoffel-lang
./examples/validate_examples.sh
```

## Common pitfalls

- Do not use clear function arguments when the program expects `ClientStore` inputs.
- Do not reorder repeated `--client-input` values for the same slot; order is the per-client input index.
- Do not omit `--expected-output-clients` for programs that call `MpcOutput.send_to_client` or `Share.send_to_client`.
- Do not reveal intermediate private values in examples unless the algorithm intentionally opens that result.
- Do not claim protocol behavior from static compilation alone; run local MPC or report the blocker.

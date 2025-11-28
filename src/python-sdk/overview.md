# Python SDK Overview

> **Status: Work in Progress**
>
> The Python SDK is currently under active development. The API described here reflects the target design. For a production-ready SDK today, see the [Rust SDK](../rust-sdk/overview.md).

The Stoffel Python SDK provides a clean, high-level interface for integrating Stoffel's secure Multi-Party Computation capabilities into Python applications. It offers a developer-friendly API that abstracts away cryptographic complexity while maintaining clear semantics for public and secret data.

## Repository

The Python SDK is being developed at: [github.com/Stoffel-Labs/stoffel-python-sdk](https://github.com/Stoffel-Labs/stoffel-python-sdk)

## Design Philosophy

The SDK is built around two core principles:

### Separation of Concerns

- **StoffelProgram**: Handles StoffelLang compilation, VM operations, and execution parameters
- **StoffelClient**: Manages MPC network communication, data handling, and result reconstruction

### Explicit Data Visibility

The API makes a clear distinction between:
- **Secret Inputs**: Private data that gets secret-shared across MPC nodes
- **Public Inputs**: Configuration and parameters visible to all nodes

## Core Components

### StoffelProgram - VM Operations

Responsible for local program management and compilation:

```python
from stoffel import StoffelProgram

# Create and compile a program
program = StoffelProgram("secure_add.stfl")
program.compile(optimize=True)

# Set execution parameters
program.set_execution_params({
    "computation_id": "secure_addition",
    "function_name": "main",
    "expected_inputs": ["a", "b", "threshold"]
})

# Test locally before MPC execution
result = program.execute_locally({"a": 25, "b": 17})
```

### StoffelClient - Network Operations

Handles MPC network communication and data management:

```python
from stoffel import StoffelClient

# Configure MPC network connection
client = StoffelClient({
    "nodes": [
        "http://mpc-node1:9000",
        "http://mpc-node2:9000",
        "http://mpc-node3:9000"
    ],
    "client_id": "client_001",
    "program_id": "secure_addition"
})

# Execute with explicit public/secret inputs
result = await client.execute_with_inputs(
    secret_inputs={"a": 25, "b": 17},      # Private data
    public_inputs={"threshold": 50}        # Public configuration
)
```

## Quick Start

### Simple MPC Computation

```python
import asyncio
from stoffel import StoffelProgram, StoffelClient

async def main():
    # 1. Program compilation and setup
    program = StoffelProgram("secure_add.stfl")
    program.compile()
    program.set_execution_params({
        "computation_id": "secure_addition",
        "function_name": "main",
        "expected_inputs": ["a", "b"]
    })

    # 2. MPC network client setup
    client = StoffelClient({
        "nodes": ["http://mpc-node1:9000", "http://mpc-node2:9000", "http://mpc-node3:9000"],
        "client_id": "my_client",
        "program_id": "secure_addition"
    })

    # 3. Execute secure computation
    result = await client.execute_with_inputs(
        secret_inputs={"a": 25, "b": 17}
    )

    print(f"Secure computation result: {result}")
    await client.disconnect()

asyncio.run(main())
```

## Development Status

Current implementation progress:

| Component | Status | Notes |
|-----------|--------|-------|
| Clean API Design | ✅ Complete | Separation of concerns implemented |
| StoffelProgram | 🚧 In Progress | Compilation and VM operations |
| StoffelClient | 🚧 In Progress | Network communication interface |
| VM Bindings | 🚧 In Progress | FFI bindings to StoffelVM |
| MPC Network Integration | 📋 Planned | Awaiting MPC service infrastructure |
| Integration Tests | 📋 Planned | With actual shared libraries |

## Current Alternative: Rust SDK

While the Python SDK is being developed, you can use the fully-functional [Rust SDK](../rust-sdk/overview.md) which provides:

- Complete compilation and VM execution
- MPC configuration with HoneyBadger protocol
- Network-based client/server architecture
- Local testing capabilities

## Contributing

The Python SDK is open source and contributions are welcome!

- **Repository**: [github.com/Stoffel-Labs/stoffel-python-sdk](https://github.com/Stoffel-Labs/stoffel-python-sdk)
- **Contributing Guide**: See [Contributing](../development/contributing.md)

## Next Steps

- **[Rust SDK Overview](../rust-sdk/overview.md)**: Use the production-ready Rust SDK today
- **[StoffelLang](../stoffel-lang/overview.md)**: Learn about the computation language
- **[CLI Templates](../cli/project-management.md)**: Python template for project scaffolding

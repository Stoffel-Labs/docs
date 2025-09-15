# Python SDK Overview

The Stoffel Python SDK provides a clean, high-level interface for integrating Stoffel's secure Multi-Party Computation capabilities into Python applications. It offers a developer-friendly API that abstracts away cryptographic complexity while maintaining clear semantics for public and secret data.

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

### Minimal One-Liner Usage

```python
import asyncio
from stoffel import StoffelClient

async def main():
    client = StoffelClient({
        "nodes": ["http://mpc-node1:9000", "http://mpc-node2:9000", "http://mpc-node3:9000"],
        "client_id": "my_client",
        "program_id": "my_secure_program"
    })

    result = await client.execute_with_inputs(
        secret_inputs={"user_data": 123, "private_value": 456},
        public_inputs={"config_param": 100}
    )

    print(f"Result: {result}")
    await client.disconnect()

asyncio.run(main())
```

## API Reference

### StoffelProgram

```python
class StoffelProgram:
    def __init__(self, source_file: Optional[str] = None)

    # Compilation and loading
    def compile(self, optimize: bool = True) -> str
    def load_program(self) -> None

    # Execution configuration
    def set_execution_params(self, params: Dict[str, Any]) -> None
    def get_computation_id(self) -> str
    def get_program_info(self) -> Dict[str, Any]

    # Local testing
    def execute_locally(self, inputs: Dict[str, Any]) -> Any
```

### StoffelClient

```python
class StoffelClient:
    def __init__(self, network_config: Dict[str, Any])

    # Recommended API - explicit input types
    async def execute_with_inputs(
        self,
        secret_inputs: Optional[Dict[str, Any]] = None,
        public_inputs: Optional[Dict[str, Any]] = None
    ) -> Any

    # Individual input management
    def set_secret_input(self, name: str, value: Any) -> None
    def set_public_input(self, name: str, value: Any) -> None
    def set_inputs(
        self,
        secret_inputs: Optional[Dict[str, Any]] = None,
        public_inputs: Optional[Dict[str, Any]] = None
    ) -> None

    # Connection management
    async def connect(self) -> None
    async def disconnect(self) -> None
    def is_ready(self) -> bool
    def get_connection_status(self) -> Dict[str, Any]

    # Legacy API (backward compatibility)
    async def execute_program_with_inputs(self, inputs: Dict[str, Any]) -> Any
    def set_private_data(self, name: str, value: Any) -> None
    async def execute_program(self) -> Any
```

## Network Configuration

### Direct Node Connection

```python
# Direct connection to known MPC nodes
client = StoffelClient({
    "nodes": [
        "http://mpc-node1:9000",
        "http://mpc-node2:9000",
        "http://mpc-node3:9000"
    ],
    "client_id": "your_client_id",
    "program_id": "your_program_id"
})
```

### Optional Coordinator Integration

```python
# With coordinator for metadata exchange
client = StoffelClient({
    "nodes": [
        "http://mpc-node1:9000",
        "http://mpc-node2:9000",
        "http://mpc-node3:9000"
    ],
    "coordinator_url": "http://coordinator:8080",  # Optional
    "client_id": "your_client_id",
    "program_id": "your_program_id"
})
```

## Usage Patterns

### Healthcare Data Privacy

```python
async def secure_health_analysis():
    client = StoffelClient(config)

    result = await client.execute_with_inputs(
        secret_inputs={
            "patient_age": 45,
            "medical_history": encoded_history,
            "test_results": lab_values
        },
        public_inputs={
            "analysis_type": "risk_assessment",
            "threshold_values": risk_thresholds
        }
    )

    return result
```

### Financial Computation

```python
async def secure_credit_score():
    client = StoffelClient(config)

    result = await client.execute_with_inputs(
        secret_inputs={
            "salary": 75000,
            "credit_history": credit_data,
            "debt_ratio": 0.3
        },
        public_inputs={
            "scoring_model": "fico_v9",
            "market_conditions": current_rates
        }
    )

    return result
```

### Multi-Party Auction

```python
async def secure_auction():
    client = StoffelClient(config)

    result = await client.execute_with_inputs(
        secret_inputs={
            "my_bid": 1000,
            "max_budget": 5000
        },
        public_inputs={
            "auction_id": "item_12345",
            "auction_rules": rules_config
        }
    )

    return result
```

## Advanced Features

### Low-Level VM Access

For specialized use cases requiring direct VM control:

```python
from stoffel.vm import VirtualMachine, StoffelValue

# Direct VM instantiation
vm = VirtualMachine()

# Register custom foreign functions
def custom_function(arg1, arg2):
    return arg1 * arg2 + 42

vm.register_foreign_function("custom_op", custom_function)

# Execute with arguments
result = vm.execute_with_args("main", [
    StoffelValue.integer(100),
    StoffelValue.string("test")
])
```

### Error Handling

```python
from stoffel.mpc import MPCError, NetworkError, ComputationError

try:
    result = await client.execute_with_inputs(
        secret_inputs={"value": 123},
        public_inputs={"param": 456}
    )
except NetworkError as e:
    print(f"Network issue: {e}")
except ComputationError as e:
    print(f"MPC computation failed: {e}")
except MPCError as e:
    print(f"General MPC error: {e}")
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- StoffelVM shared library (`libstoffel_vm.so` or equivalent)
- StoffelLang compiler (for `.stfl` compilation)

### Installation Options

```bash
# With Poetry (recommended)
poetry install

# With pip
pip install stoffel-python-sdk

# Development installation
git clone https://github.com/stoffel-labs/stoffel-python-sdk.git
cd stoffel-python-sdk
poetry install
```

## Examples and Testing

The SDK includes comprehensive examples:

```bash
# Simple API demonstration
poetry run python examples/simple_api_demo.py

# Complete architecture example
poetry run python examples/correct_flow.py

# Advanced VM operations
poetry run python examples/vm_example.py
```

## Development Status

Current implementation status:

- ✅ **Clean API Design**: Proper separation of concerns implemented
- ✅ **StoffelProgram**: Compilation and VM operations (ready for integration)
- ✅ **StoffelClient**: Network communication interface (ready for MPC integration)
- ✅ **VM Bindings**: FFI bindings to StoffelVM
- 🚧 **MPC Network Integration**: Awaiting actual MPC service infrastructure
- 🚧 **StoffelLang Integration**: Compiler integration in progress
- 📋 **Integration Tests**: With actual shared libraries and MPC networks

## Architecture Benefits

### Clean Separation

- **VM Operations**: Isolated in StoffelProgram for local testing and compilation
- **Network Communication**: Handled by StoffelClient for MPC operations
- **Clear Boundaries**: Easy to understand and extend

### Type Safety

- **Explicit Input Types**: Clear distinction between secret and public data
- **Runtime Safety**: Proper error handling and validation
- **Development Safety**: Type hints throughout the codebase

### Extensibility

- **Plugin Architecture**: Ready for additional protocol backends
- **Foreign Functions**: Easy integration with existing Python libraries
- **Modular Design**: Components can be used independently

## Next Steps

To get started with the Stoffel Python SDK:

- **[Installation](./installation.md)**: Set up the development environment
- **[API Reference](./api.md)**: Detailed API documentation
- **[Examples](./examples.md)**: Comprehensive usage examples
# Rust SDK Overview

The Stoffel Rust SDK provides a high-level API for building Multi-Party Computation (MPC) applications in Rust. It bridges the StoffelLang compiler, StoffelVM execution engine, and HoneyBadger MPC protocol into a cohesive, developer-friendly interface.

## Design Philosophy

The SDK is built around three core principles:

### Progressive Disclosure

Three API levels for different needs:
- **Simple API**: Quick compilation and local testing
- **Builder Pattern**: Full MPC configuration
- **Advanced API**: Direct access to network and protocol layers

### MPC-First Design

Programs are configured for MPC during compilation, ensuring all participants use consistent parameters.

### Clean Abstractions

The SDK hides cryptographic complexity while providing clear semantics for secret and public data.

## MPCaaS Architecture

The SDK implements an **MPC-as-a-Service (MPCaaS)** architecture that separates app developers from infrastructure operators:

```
┌─────────────────────────────────────────────────────────────┐
│                     App Developers                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              StoffelClient                            │   │
│  │  - Simple API: submit inputs, get outputs            │   │
│  │  - Auto-discovers network configuration              │   │
│  │  - No MPC knowledge required                         │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                 Infrastructure Operators                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              StoffelServer                            │   │
│  │  - Full mesh peer connections                        │   │
│  │  - HoneyBadger preprocessing                         │   │
│  │  - Handles secure computation                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### StoffelClient (For App Developers)

```rust
use stoffel_rust_sdk::prelude::*;

async fn submit_computation() -> Result<i64> {
    // Connect to MPC network
    let client = StoffelClient::builder()
        .with_servers(&["mpc1.example.com:9000", "mpc2.example.com:9000"])
        .client_id(12345)
        .connect()
        .await?;

    // Submit inputs and get result
    let result = client.run(&[42, 100]).await?;

    Ok(result)
}
```

### StoffelServer (For Infrastructure Operators)

```rust
use stoffel_rust_sdk::prelude::*;

async fn run_mpc_server(party_id: usize) -> Result<()> {
    // Load compiled program
    let program = Stoffel::compile_file("program.stfl")?.build()?;

    // Build and configure server
    let server = Stoffel::server(party_id)
        .bind("0.0.0.0:9000")
        .with_peers(&[
            (0, "peer0.example.com:9000"),
            (1, "peer1.example.com:9000"),
            (2, "peer2.example.com:9000"),
        ])
        .with_program(program.program().clone())
        .with_preprocessing(3, 8)  // triples, random shares
        .with_instance_id(12345)
        .build()?;

    // Start serving
    server.start().await?;
    server.connect_to_peers().await?;
    server.run_forever().await
}
```

### QUIC Networking

All network communication uses QUIC for:
- **TLS 1.3 encryption**: Secure by default
- **Stream multiplexing**: Efficient message handling
- **Low latency**: 0-RTT connection establishment
- **Connection migration**: Handles network changes

## Quick Start

### Simple Local Execution

```rust
use stoffel_rust_sdk::prelude::*;

fn main() -> Result<()> {
    let source = r#"
        def add(a: int64, b: int64) -> int64:
            return a + b

        main main() -> int64:
            return add(10, 20)
    "#;

    let result = Stoffel::compile(source)?
        .execute_local()?;

    println!("Result: {:?}", result);
    Ok(())
}
```

### MPC Configuration

```rust
use stoffel_rust_sdk::prelude::*;

fn main() -> Result<()> {
    let runtime = Stoffel::compile(source)?
        .parties(5)           // 5-party MPC network
        .threshold(1)         // Byzantine fault tolerance
        .instance_id(42)      // Unique computation ID
        .build()?;

    // Test locally before deployment
    let result = runtime.program().execute_local()?;
    println!("Local test result: {:?}", result);

    Ok(())
}
```

### Creating MPC Participants

```rust
use stoffel_rust_sdk::prelude::*;

async fn setup_mpc() -> Result<()> {
    let runtime = Stoffel::compile(source)?
        .parties(5)
        .threshold(1)
        .build()?;

    // Create an MPC server (compute node)
    let server = runtime.server(0)
        .with_preprocessing(10, 25)  // 10 triples, 25 random shares
        .build()?;

    // Create an MPC client (input provider)
    let client = runtime.client(100)
        .with_inputs(vec![10, 20])
        .build()?;

    Ok(())
}
```

## Core Components

### Stoffel Builder

The entry point for all SDK operations:

```rust
Stoffel::compile(source)      // Compile from string
Stoffel::compile_file(path)   // Compile from file
Stoffel::load(bytecode)       // Load pre-compiled bytecode
```

### StoffelRuntime

After building, provides access to:

```rust
let runtime = Stoffel::compile(source)?.build()?;

runtime.program()      // Access compiled bytecode
runtime.client(id)     // Create MPC client builder
runtime.server(id)     // Create MPC server builder
runtime.node(id)       // Create MPC node builder (client + server)
```

### Program

Pure bytecode container with execution methods:

```rust
let program = runtime.program();

program.execute_local()?;                    // Run main function
program.execute_local_function("func")?;     // Run specific function
program.list_functions()?;                   // List available functions
program.save("output.stfb")?;                // Save bytecode to file
```

### MPC Participants

Three participant types for different roles:

| Type | Provides Inputs | Computes | Receives Outputs |
|------|-----------------|----------|------------------|
| **MPCClient** | ✓ | ✗ | ✓ |
| **MPCServer** | ✗ | ✓ | ✗ |
| **MPCNode** | ✓ | ✓ | ✓ |

## MPC Configuration

### Protocol Parameters

```rust
Stoffel::compile(source)?
    .parties(5)                          // Number of parties (min: 4)
    .threshold(1)                        // Fault tolerance
    .instance_id(42)                     // Computation instance
    .protocol(ProtocolType::HoneyBadger) // MPC protocol
    .share_type(ShareType::Robust)       // Secret sharing scheme
    .build()?
```

### Validation Rules

The SDK automatically validates MPC parameters:

- **HoneyBadger**: Requires `n >= 3t + 1` where `n` = parties, `t` = threshold
- Minimum 4 parties with threshold 1
- Common configurations:
  - 4 parties, threshold 1: `4 >= 4` ✓
  - 5 parties, threshold 1: `5 >= 4` ✓ (recommended default)
  - 7 parties, threshold 2: `7 >= 7` ✓

## Error Handling

The SDK provides comprehensive error types:

```rust
use stoffel_rust_sdk::error::{Error, Result};

match Stoffel::compile(source)?.build() {
    Ok(runtime) => { /* success */ }
    Err(Error::CompilationError(msg)) => { /* syntax error */ }
    Err(Error::Configuration(msg)) => { /* invalid MPC params */ }
    Err(Error::Network(msg)) => { /* connection error */ }
    Err(e) => { /* other error */ }
}
```

Error categories:
- `CompilationError`: StoffelLang syntax or semantic errors
- `RuntimeError`: VM execution failures
- `MPCError`: Protocol-level errors
- `Configuration`: Invalid parameters
- `Network`: Connection failures
- `IoError`: File operations

## Network Configuration

### Programmatic Configuration

```rust
let runtime = Stoffel::compile(source)?
    .parties(5)
    .threshold(1)
    .build()?;

let server = runtime.server(0).build()?;
server.add_peer(1, "127.0.0.1:19201".parse()?);
server.bind_and_listen("127.0.0.1:19200".parse()?).await?;
```

### TOML Configuration

```toml
# stoffel.toml
[network]
party_id = 0
bind_address = "127.0.0.1:9001"
bootstrap_address = "127.0.0.1:9000"
min_parties = 4

[mpc]
n_parties = 5
threshold = 1
instance_id = 12345
```

```rust
let runtime = Stoffel::compile(source)?
    .network_config_file("stoffel.toml")?
    .build()?;
```

## Next Steps

- **[Installation](./installation.md)**: Set up the Rust SDK
- **[API Reference](./api.md)**: Complete API documentation
- **[Examples](./examples.md)**: Working code examples
- **[StoffelLang](../stoffel-lang/overview.md)**: Learn the computation language

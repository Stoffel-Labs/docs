# Installation

## Prerequisites

- Rust 1.70 or higher
- Git (for submodule dependencies)
- Stoffel CLI (optional, for project scaffolding)

## Installation Methods

### Using Cargo (Recommended)

Add to your `Cargo.toml`:

```toml
[dependencies]
stoffel-rust-sdk = { git = "https://github.com/Stoffel-Labs/stoffel-rust-sdk" }
```

Then run:

```bash
cargo build
```

### Using Stoffel CLI Template

The easiest way to start a new Rust MPC project:

```bash
# Install Stoffel CLI first (see Getting Started)
stoffel init my-mpc-app --template rust
cd my-mpc-app
cargo build
```

This creates a complete project with:
- Rust application with SDK integration
- StoffelLang program in `stoffel/src/program.stfl`
- Example code demonstrating the SDK API
- Ready-to-run configuration

### From Source

For development or customization:

```bash
git clone https://github.com/Stoffel-Labs/stoffel-rust-sdk.git
cd stoffel-rust-sdk

# Initialize submodules (required)
git submodule update --init --recursive

cargo build
cargo test
```

## Verifying Installation

Create a simple test program:

```rust
use stoffel_rust_sdk::prelude::*;

fn main() -> Result<()> {
    let source = r#"
        main main() -> int64:
            return 42
    "#;

    let result = Stoffel::compile(source)?
        .execute_local()?;

    println!("Result: {:?}", result);
    Ok(())
}
```

Run it:

```bash
cargo run
```

Expected output:
```
Result: I64(42)
```

## Dependencies

The SDK depends on several Stoffel components (managed as git submodules):

| Component | Purpose |
|-----------|---------|
| `stoffellang` | StoffelLang compiler |
| `stoffel-vm` | Virtual machine runtime |
| `stoffelmpc-mpc` | HoneyBadger MPC protocol |
| `stoffelnet` | QUIC networking |

These are automatically fetched when you add the SDK as a dependency.

## Platform Support

| Platform | Status |
|----------|--------|
| Linux (x86_64) | ✅ Fully supported |
| macOS (x86_64, ARM64) | ✅ Fully supported |
| Windows (WSL2) | ✅ Supported |
| Windows (native) | ⚠️ Experimental |

## Troubleshooting

### Submodule Issues

If you see errors about missing dependencies:

```bash
git submodule update --init --recursive
```

### Build Failures

Ensure you have the latest Rust:

```bash
rustup update stable
```

### Linking Errors

On Linux, you may need:

```bash
sudo apt-get install build-essential pkg-config libssl-dev
```

On macOS:

```bash
xcode-select --install
```

## Next Steps

- **[SDK Overview](./overview.md)**: Understand the SDK architecture
- **[API Reference](./api.md)**: Complete API documentation
- **[Examples](./examples.md)**: Working code examples

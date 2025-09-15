# Stoffel CLI Overview

The Stoffel CLI is a comprehensive command-line interface that provides everything you need to develop, build, and deploy privacy-preserving applications using secure Multi-Party Computation (MPC).

## Design Philosophy

The Stoffel CLI is designed with the following principles:

- **Developer-Friendly**: Intuitive commands that follow familiar patterns from tools like `cargo` and `npm`
- **Template-Driven**: Project templates for different use cases and programming languages
- **Integrated Workflow**: Seamless integration between development, compilation, and deployment
- **Extensible**: Plugin system for future enhancements and community contributions

## Core Commands

### Project Management

```bash
# Initialize new projects
stoffel init my-project                    # Default StoffelLang project
stoffel init --template python webapp      # Python integration template
stoffel init --lib crypto-utils           # Create a library project
stoffel init --interactive                # Interactive project setup
```

### Compilation

```bash
# Compile StoffelLang programs
stoffel compile                            # Compile all files in src/
stoffel compile src/main.stfl              # Compile specific file
stoffel compile --binary                   # Generate VM-compatible binaries
stoffel compile -O3                        # Maximum optimization
```

### Development

```bash
# Development server with hot reloading
stoffel dev                                # Default: 5 parties, port 8080
stoffel dev --parties 7 --port 3000       # Custom configuration
stoffel dev --field bn254                 # Different cryptographic field
```

### Building and Deployment

```bash
# Build for different targets
stoffel build                              # Debug build
stoffel build --release                    # Production build
stoffel build --target wasm               # WebAssembly target

# Deploy to various environments
stoffel deploy --target tee               # TEE deployment
stoffel deploy --env production           # Production environment
```

## Available Templates

The CLI provides templates for different development scenarios:

### Language-Specific Templates

- **`python`**: Full Python SDK integration with Poetry and pytest
- **`rust`**: Rust FFI integration with StoffelVM (development skeleton)
- **`typescript`**: TypeScript/Node.js client integration
- **`solidity`**: Smart contracts with MPC result verification

### Use-Case Templates

- **`web3-auction`**: Private auction implementation
- **`web3-voting`**: Secure voting system
- **`web-healthcare`**: Healthcare data privacy
- **`web-fintech`**: Financial computation privacy
- **`desktop-messaging`**: Secure messaging application

## Project Structure

When you create a new project, the CLI generates a standard structure:

```
my-mpc-project/
├── Stoffel.toml              # Project configuration
├── src/                      # StoffelLang source files
│   ├── main.stfl            # Main program entry point
│   └── lib.stfl             # Library functions (for --lib projects)
├── tests/                   # Test files
│   └── integration.stfl     # Integration tests
└── README.md               # Project documentation
```

### Python Template Structure

For Python integration projects:

```
my-python-project/
├── Stoffel.toml             # Stoffel configuration
├── pyproject.toml           # Poetry configuration
├── src/
│   ├── main.py             # Python implementation
│   └── secure_computation.stfl  # StoffelLang program
├── tests/
│   └── test_main.py        # Python tests
└── README.md
```

## Configuration

### Stoffel.toml

The main configuration file for Stoffel projects:

```toml
[package]
name = "my-secure-app"
version = "0.1.0"
authors = ["Your Name <you@example.com>"]
edition = "2024"

[mpc]
protocol = "honeybadger"
parties = 5
threshold = 1
field = "bls12-381"

[build]
optimization_level = 2
target = "vm"
output_dir = "build"

[dev]
hot_reload = true
simulation_mode = true
port = 8080

[dependencies]
# Future: Package dependencies will be listed here
```

## MPC Configuration

The CLI supports configurable MPC parameters:

- **Parties**: Number of parties in the MPC computation (minimum 5 for security)
- **Threshold**: Maximum number of corrupted parties = `(parties - 1) / 3`
- **Cryptographic Fields**: BLS12-381 (default), BN254, Secp256k1, Prime61
- **Protocol**: Currently HoneyBadger MPC (more protocols planned)

## Development Server Features

The `stoffel dev` command provides:

- **Hot Reloading**: Automatic recompilation and restart when files change
- **MPC Simulation**: Local simulation of multi-party computation for testing
- **Debug Interface**: Web interface for debugging MPC execution
- **Live Logs**: Real-time logs from all simulated parties
- **Performance Metrics**: Timing and communication overhead analysis

## Help System

The CLI provides comprehensive help for all commands:

```bash
stoffel --help                    # Main help
stoffel init --help               # Command-specific help
stoffel compile --binary --help   # Flag-specific help
```

## Future Features

Planned enhancements for the CLI:

- **Package Manager**: `stoffel add` and `stoffel publish` for dependency management
- **Testing Framework**: `stoffel test` with MPC-specific test patterns
- **Deployment Tools**: Enhanced deployment to cloud providers and Kubernetes
- **Plugin System**: Community plugins for specialized workflows
- **IDE Integration**: Language server protocol support for editors

## Examples

### Quick Start

```bash
# Create and run a simple MPC project
stoffel init hello-mpc
cd hello-mpc
stoffel dev

# In another terminal
curl http://localhost:8080/execute
```

### Python Integration

```bash
# Create Python project with MPC
stoffel init secure-analytics --template python
cd secure-analytics

# Install Python dependencies
poetry install

# Start development
stoffel dev --parties 7
```

### Production Deployment

```bash
# Build optimized release
stoffel build --release --target production

# Deploy to TEE environment
stoffel deploy --target tee --config production.toml
```

## Next Steps

- **[Project Management](./project-management.md)**: Learn about creating and managing projects
- **[Development Workflow](./development.md)**: Understand the development process
- **[Building and Deployment](./building.md)**: Build and deploy your applications
# Ecosystem Overview

The Stoffel ecosystem provides a complete toolchain for developing privacy-preserving applications using secure Multi-Party Computation (MPC). This page provides an overview of how the different components work together.

## Component Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Stoffel CLI   │    │  StoffelLang    │    │   Python SDK    │
│                 │    │   Compiler      │    │                 │
│ Project Mgmt    │───▶│                 │    │ StoffelProgram  │
│ Build Tools     │    │ .stfl → .stfb   │    │ StoffelClient   │
│ Dev Server      │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │   StoffelVM     │              │
         │              │                 │              │
         └─────────────▶│ Register-based  │◀─────────────┘
                        │ Virtual Machine │
                        │ MPC Optimized   │
                        └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ MPC Protocols   │
                        │                 │
                        │ HoneyBadger MPC │
                        │ Rust Implementation│
                        └─────────────────┘
```

## Development Workflow

### 1. Project Initialization
Use the Stoffel CLI to create new projects with appropriate templates:

```bash
# Create a new MPC project with Python integration
stoffel init my-secure-app --template python

# Create a pure StoffelLang project
stoffel init privacy-lib --lib
```

### 2. Development
Write your privacy-preserving logic in StoffelLang and integrate with your preferred language:

**StoffelLang Program (`src/secure_add.stfl`)**:
```javascript
fn secure_add(a: secret i32, b: secret i32) -> secret i32 {
    return a + b;
}

fn main() {
    let result = secure_add(25, 17);
    reveal(result);
}
```

**Python Integration**:
```python
from stoffel import StoffelProgram, StoffelClient

# Compile and execute
program = StoffelProgram("src/secure_add.stfl")
program.compile()

client = StoffelClient(config)
result = await client.execute_with_inputs(
    secret_inputs={"a": 25, "b": 17}
)
```

### 3. Development Server
Run the development server for hot reloading and MPC simulation:

```bash
stoffel dev --parties 5 --port 3000
```

### 4. Building and Deployment
Build optimized binaries for production:

```bash
# Create production build
stoffel build --release

# Deploy to TEE environment
stoffel deploy --target tee --env production
```

## Component Details

### Stoffel CLI
The central command-line interface that orchestrates the entire development workflow:

- **Project Management**: Initialize projects with templates for different use cases
- **Compilation**: Compile StoffelLang programs to VM bytecode
- **Development**: Hot-reloading server with MPC simulation
- **Build System**: Optimize and package applications for deployment
- **Deployment**: Deploy to various targets including TEE and cloud environments

### StoffelLang Compiler
A modern programming language designed specifically for MPC:

- **Syntax**: Inspired by Rust, Python, and JavaScript for familiar development experience
- **Type System**: Strong static typing with inference, supporting both clear and secret types
- **Compilation**: Generates optimized bytecode compatible with StoffelVM
- **Integration**: Works seamlessly with the CLI and other ecosystem components

### StoffelVM
A register-based virtual machine optimized for multiparty computation:

- **Architecture**: Separate clear and secret registers for efficient MPC operations
- **Instructions**: Comprehensive instruction set for arithmetic, control flow, and memory operations
- **Types**: Rich type system including primitives, objects, arrays, and closures
- **Runtime**: Hook system for debugging and protocol integration

### Python SDK
High-level Python interface for integrating Stoffel into existing applications:

- **StoffelProgram**: Handles compilation, VM operations, and execution parameters
- **StoffelClient**: Manages MPC network communication and data handling
- **API Design**: Clean separation of concerns with explicit public/secret input handling
- **Integration**: Easy integration into existing Python codebases

### MPC Protocols
Rust implementation of secure multiparty computation protocols:

- **HoneyBadger MPC**: Primary protocol implementation for secure computation
- **Cryptographic Fields**: Support for multiple fields (BLS12-381, BN254, etc.)
- **Security**: Configurable security parameters and threshold settings
- **Performance**: Optimized for practical MPC applications

## Integration Patterns

### Standalone Applications
For new applications built entirely with Stoffel:

```bash
stoffel init secure-voting-app
cd secure-voting-app
stoffel dev
```

### Library Integration
For adding privacy features to existing applications:

```bash
cd existing-project
stoffel init --lib --path ./privacy-module
```

### Multiple Language Support
Templates available for different development environments:

- **Python**: Full SDK integration with Poetry and pytest
- **Rust**: FFI integration with StoffelVM
- **TypeScript**: Node.js client integration
- **Solidity**: Smart contract integration with MPC result verification

## Security Model

The Stoffel ecosystem provides security through:

- **Type Safety**: Clear distinction between public and secret data at the language level
- **Protocol Security**: Proven MPC protocols with configurable security parameters
- **Deployment Security**: TEE integration and secure deployment practices
- **Development Security**: Simulation environment for testing without exposing real secrets

## Next Steps

To start working with the Stoffel ecosystem:

1. **[Install Stoffel](../getting-started/installation.md)** - Set up the development environment
2. **[Create Your First Project](../getting-started/first-project.md)** - Build a simple MPC application
3. **[Learn StoffelLang](../stoffel-lang/overview.md)** - Master the programming language
4. **[Explore the CLI](../cli/overview.md)** - Understand all available commands and options
5. **[Use the Python SDK](../python-sdk/overview.md)** - Integrate with Python applications
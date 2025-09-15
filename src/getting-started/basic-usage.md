# Basic Usage

This guide covers the essential Stoffel CLI commands and workflows you'll use in your daily development. After completing the [Quick Start](./quick-start.md), you should be familiar with basic project creation and development.

## Core Workflow

The typical Stoffel development workflow follows this pattern:

```bash
stoffel init → edit code → stoffel compile → stoffel-run → repeat
```

> **Note**: Advanced workflow commands like `stoffel dev`, `stoffel test`, `stoffel build`, and `stoffel deploy` are under development.

Let's explore each command in detail.

## Project Management

### Creating Projects

```bash
# Basic project creation
stoffel init my-project

# Using templates
stoffel init py-app --template python
stoffel init rust-app --template rust
stoffel init web-app --template typescript

# Library projects
stoffel init crypto-utils --lib

# Interactive setup
stoffel init --interactive
```

#### Template Options

```bash
# List all available templates
stoffel templates list

# Get template details
stoffel templates show python

# Create template with specific options
stoffel init solidity-app --template solidity
```

### Project Structure

A typical Stoffel project looks like:

```
my-project/
├── Stoffel.toml              # Project configuration
├── src/                      # StoffelLang source files
│   ├── main.stfl            # Main program
│   ├── lib.stfl             # Library functions
│   └── utils/               # Module organization
│       └── crypto.stfl
├── tests/                   # Test files
│   ├── unit.stfl           # Unit tests
│   └── integration.stfl     # Integration tests
├── build/                   # Compiled outputs (generated)
├── .stoffel/               # Local configuration (gitignored)
└── README.md
```

### Configuration

The `Stoffel.toml` file controls project settings:

```toml
[package]
name = "my-project"
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
log_level = "info"

[dependencies]
# Future: MPC libraries will be listed here

[dev-dependencies]
# Development-only dependencies
```

## Development Commands

### Compilation

```bash
# Compile all source files in src/
stoffel compile

# Compile specific file
stoffel compile src/main.stfl

# Compile with different optimization levels
stoffel compile -O0  # No optimization (fastest compile)
stoffel compile -O1  # Basic optimization
stoffel compile -O2  # Standard optimization (default)
stoffel compile -O3  # Maximum optimization (slower compile)

# Generate VM-compatible binaries
stoffel compile --binary
stoffel compile src/main.stfl --binary --output program.stfb

# Show intermediate representations during compilation
stoffel compile --print-ir

# Disassemble compiled binaries
stoffel compile compiled.stfb --disassemble
```

#### Compilation Outputs

```bash
# After compilation, you'll find:
main.stfbin                    # VM-compatible binary (when using --binary)
```

### Execution

```bash
# Execute compiled programs (use .bin files for VM execution)
stoffel-run program.stfbin main

# Execute with command line arguments
stoffel-run program.stfbin main arg1 arg2

# Debug execution with tracing
stoffel-run program.stfbin main --trace-instr    # Trace instructions
stoffel-run program.stfbin main --trace-regs     # Trace register operations
stoffel-run program.stfbin main --trace-stack    # Trace function calls

# Combined debugging
stoffel-run program.stfbin main --trace-instr --trace-regs --trace-stack
```

### Development Workflow

For iterative development, use this pattern:

```bash
# 1. Edit your StoffelLang source files

# 2. Compile your changes
stoffel compile src/main.stfl --binary --output program.stfbin

# 3. Test execution
stoffel-run program.stfbin main

# 4. Debug if needed
stoffel-run program.stfbin main --trace-instr

# 5. Repeat
```

> **Coming Soon**: The integrated development server (`stoffel dev`) with hot reloading, web interface, and MPC simulation is under development.

### Testing

> **Coming Soon**: The integrated testing framework (`stoffel test`) is under development.

For now, test your programs manually:

```bash
# Create test programs in tests/ directory
# Compile and run them individually
stoffel compile tests/test_addition.stfl --binary --output test_addition.stfbin
stoffel-run test_addition.stfbin main

# Use tracing to verify behavior
stoffel-run test_addition.stfbin main --trace-instr --trace-regs
```

## Building and Deployment

### Building Projects

> **Coming Soon**: The integrated build system (`stoffel build`) and deployment tools (`stoffel deploy`) are under development.

For now, use the compilation workflow:

```bash
# Build for production (with maximum optimization)
stoffel compile src/main.stfl --binary --output production.stfbin -O3

# Verify the build
stoffel-run production.stfbin main

# Disassemble to inspect the compiled output
stoffel compile production.stfbin --disassemble
```

## Utility Commands

### Information and Help

```bash
# Show CLI help
stoffel --help

# Show compilation help
stoffel compile --help

# Show version information
stoffel --version

# Show help for specific flags
stoffel help compile -O      # Optimization levels
stoffel help compile --binary # Binary output format
```

### Template Management

> **Coming Soon**: Most advanced CLI features are under development.

Available template operations:

```bash
# List available templates
stoffel templates list

# Show template details
stoffel templates show python
```

## Advanced Usage

### Multi-File Projects

For projects with multiple StoffelLang files:

```bash
# Compile all files in src/ directory
stoffel compile

# This compiles all .stfl files found in src/
# Each file is compiled independently
```

### Optimization Levels

```bash
# Development: Fast compilation, no optimization
stoffel compile -O0

# Balanced: Some optimization, reasonable compile time
stoffel compile -O2

# Production: Maximum optimization, slower compilation
stoffel compile -O3 --binary --output optimized.stfbin
```

### Debugging and Analysis

```bash
# View intermediate representations
stoffel compile src/main.stfl --print-ir

# Disassemble compiled bytecode
stoffel compile program.stfbin --disassemble

# Runtime debugging with comprehensive tracing
stoffel-run program.stfbin main --trace-instr --trace-regs --trace-stack
```

## Common Workflows

### Daily Development

```bash
# 1. Edit your StoffelLang files in src/
# 2. Compile frequently during development
stoffel compile src/main.stfl --binary --output program.stfbin

# 3. Test your changes
stoffel-run program.stfbin main

# 4. Debug when needed
stoffel-run program.stfbin main --trace-instr

# 5. Version control
git add . && git commit -m "Update MPC logic"
```

### Debugging Issues

```bash
# Compilation problems
stoffel compile src/main.stfl --print-ir    # Show compilation details

# Runtime issues
stoffel-run program.stfbin main --trace-instr --trace-regs --trace-stack

# Understanding bytecode
stoffel compile program.stfbin --disassemble
```

### Production Preparation

```bash
# Create optimized build
stoffel compile src/main.stfl --binary --output production.stfbin -O3

# Verify it works
stoffel-run production.stfbin main

# Inspect the optimized bytecode
stoffel compile production.stfbin --disassemble
```

## Shell Integration

### Useful Aliases

Add to your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
# Common aliases
alias sc='stoffel compile'
alias sr='stoffel-run'
alias si='stoffel init'

# Useful functions
function stoffel-new() {
    stoffel init "$1" --template "${2:-python}"
    cd "$1"
}

function stoffel-compile-run() {
    stoffel compile "$1" --binary --output "${1%.stfl}.stfbin" && \
    stoffel-run "${1%.stfl}.stfbin" main
}
```

## Next Steps

Now that you understand basic Stoffel usage:

1. **[Your First MPC Project](./first-project.md)**: Build a complete real-world application
2. **[CLI Overview](../cli/overview.md)**: Detailed CLI reference and advanced features
3. **[StoffelLang Overview](../stoffel-lang/overview.md)**: Learn the programming language in depth
4. **[Architecture Overview](../architecture/system.md)**: Understand how Stoffel works internally

## Troubleshooting

### Common Issues

**Compilation Failures**
```bash
# Check syntax and get detailed error output
stoffel compile src/main.stfl --print-ir

# Verify file paths and structure
ls src/  # Make sure .stfl files exist

# Try compiling individual files to isolate issues
stoffel compile src/main.stfl --binary --output test.stfbin
```

**Runtime Errors**
```bash
# Use comprehensive tracing to debug
stoffel-run program.stfbin main --trace-instr --trace-regs --trace-stack

# Check that the binary was created correctly
ls -la *.stfbin

# Verify entry function exists
stoffel compile program.stfbin --disassemble | grep -i main
```

**Performance Issues**
```bash
# Use minimal optimization during development
stoffel compile src/main.stfl -O0 --binary --output debug.stfbin

# For production, use maximum optimization
stoffel compile src/main.stfl -O3 --binary --output production.stfbin
```

**Path Issues**
```bash
# Make sure you're in the project directory
pwd
ls  # Should see Stoffel.toml and src/ directory

# Check available help
stoffel --help
stoffel compile --help
```

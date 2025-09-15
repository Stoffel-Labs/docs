# Installation

This guide will help you install Stoffel from source. Since Stoffel is currently in active development, you'll need to build the components manually from their Git repositories.

## Prerequisites

### System Requirements

**Operating Systems**
- Linux (Ubuntu 20.04+, CentOS 8+, Arch Linux)
- macOS (10.15+)
- Windows (via WSL2 recommended)

**Hardware Requirements**
- 4GB RAM minimum (8GB recommended for MPC development)
- 2GB free disk space
- Internet connection for downloading dependencies

### Required Dependencies

Before installing Stoffel, make sure you have:

**Essential Tools**
- **Git** (for cloning repositories)
- **Rust and Cargo** (latest stable version)

**Optional (based on your use case)**
- **Python 3.8+** (for Python SDK integration)

## Step-by-Step Installation

### Step 1: Install Rust

If you don't have Rust installed:

```bash
# Install Rust and Cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Source the environment
source ~/.cargo/env

# Verify installation
rustc --version
cargo --version
```

### Step 2: Create a Stoffel Workspace

```bash
# Create a directory for all Stoffel components
mkdir ~/stoffel-dev
cd ~/stoffel-dev
```

### Step 3: Clone the Repositories

Clone all the Stoffel components:

```bash
# Clone the main Stoffel CLI
git clone https://github.com/Stoffel-Labs/Stoffel.git

# Clone StoffelVM
git clone https://github.com/Stoffel-Labs/StoffelVM.git

# Clone Stoffel-Lang compiler
git clone https://github.com/Stoffel-Labs/Stoffel-Lang.git

# Clone MPC protocols
git clone https://github.com/Stoffel-Labs/mpc-protocols.git

# Clone Python SDK (optional)
git clone https://github.com/Stoffel-Labs/stoffel-python-sdk.git
```

Your directory structure should look like:
```
~/stoffel-dev/
├── Stoffel/                  # Main CLI
├── StoffelVM/               # Virtual Machine
├── Stoffel-Lang/            # Language compiler
├── mpc-protocols/           # MPC protocol implementations
└── stoffel-python-sdk/      # Python SDK (optional)
```

### Step 4: Build the Components

Build each component in the correct order:

#### Build StoffelVM First

```bash
cd ~/stoffel-dev/StoffelVM

# Build the VM
cargo build --release

# Verify the build
./target/release/stoffel-run --version
```

#### Build Stoffel-Lang Compiler

```bash
cd ~/stoffel-dev/Stoffel-Lang

# Build the compiler
cargo build --release

# Verify the build
./target/release/stoffellang --version
```

#### Build MPC Protocols

```bash
cd ~/stoffel-dev/mpc-protocols

# Build the protocols
cargo build --release
```

#### Build the Main Stoffel CLI

```bash
cd ~/stoffel-dev/Stoffel

# Build the CLI
cargo build --release

# Verify the build
./target/release/stoffel --version
```

### Step 5: Install to Your System

Add the built binaries to your PATH:

```bash
# Create a bin directory in your home folder
mkdir -p ~/.local/bin

# Copy the binaries
cp ~/stoffel-dev/Stoffel/target/release/stoffel ~/.local/bin/
cp ~/stoffel-dev/StoffelVM/target/release/stoffel-run ~/.local/bin/
cp ~/stoffel-dev/Stoffel-Lang/target/release/stoffellang ~/.local/bin/

# Add to your PATH (add this to your ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload your shell or source the profile
source ~/.bashrc  # or ~/.zshrc for zsh
```

### Step 6: Verify Installation

Test that everything is working:

```bash
# Test Stoffel CLI
stoffel --version

# Test StoffelLang compiler
stoffellang --version

# Test StoffelVM
stoffel-run --version

# Test basic functionality
stoffel --help
```

## Python SDK Installation (Optional)

If you want to use the Python SDK:

```bash
# Navigate to the Python SDK directory
cd ~/stoffel-dev/stoffel-python-sdk

# Install in development mode
pip install -e .

# Or create a virtual environment first (recommended)
python -m venv venv
source venv/bin/activate
pip install -e .

# Verify installation
python -c "import stoffel; print('Python SDK installed successfully')"
```

## Development Setup

For development work, you can run the tools directly from their build directories:

```bash
# Create aliases for easier development (add to ~/.bashrc or ~/.zshrc)
alias stoffel-dev='~/stoffel-dev/Stoffel/target/release/stoffel'
alias stoffellang-dev='~/stoffel-dev/Stoffel-Lang/target/release/stoffellang'
alias stoffel-run-dev='~/stoffel-dev/StoffelVM/target/release/stoffel-run'
```

## Keeping Up to Date

To update your Stoffel installation:

```bash
# Update each repository
cd ~/stoffel-dev/Stoffel && git pull && cargo build --release
cd ~/stoffel-dev/StoffelVM && git pull && cargo build --release
cd ~/stoffel-dev/Stoffel-Lang && git pull && cargo build --release
cd ~/stoffel-dev/mpc-protocols && git pull && cargo build --release

# Copy updated binaries
cp ~/stoffel-dev/Stoffel/target/release/stoffel ~/.local/bin/
cp ~/stoffel-dev/StoffelVM/target/release/stoffel-run ~/.local/bin/
cp ~/stoffel-dev/Stoffel-Lang/target/release/stoffellang ~/.local/bin/
```

## Troubleshooting

### Common Issues

#### Rust/Cargo not found

```bash
# Make sure Rust is properly installed
which cargo
cargo --version

# If not found, reinstall Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

#### Build errors

```bash
# Make sure you have the latest Rust version
rustup update

# Clean and rebuild
cargo clean
cargo build --release
```

#### Command not found after installation

```bash
# Check if binaries are in the right place
ls -la ~/.local/bin/stoffel*

# Make sure PATH is set correctly
echo $PATH | grep -q "$HOME/.local/bin" && echo "PATH is correct" || echo "PATH needs updating"

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Permission issues

```bash
# Make sure binaries are executable
chmod +x ~/.local/bin/stoffel*
```

### Getting Help

If you encounter issues:

1. **Check the individual repository README files** for component-specific instructions
2. **GitHub Issues**: Report issues at the respective repository
   - [Stoffel CLI Issues](https://github.com/Stoffel-Labs/Stoffel/issues)
   - [StoffelVM Issues](https://github.com/Stoffel-Labs/StoffelVM/issues)
   - [Stoffel-Lang Issues](https://github.com/Stoffel-Labs/Stoffel-Lang/issues)
3. **Build logs**: Check cargo output for specific error messages

## Next Steps

Now that you have Stoffel installed:

1. **[Quick Start](./quick-start.md)**: Create your first project in 5 minutes
2. **[Basic Usage](./basic-usage.md)**: Learn the essential Stoffel commands
3. **[Your First MPC Project](./first-project.md)**: Build a complete privacy-preserving application

## Development Workflow

For contributors or those wanting to modify Stoffel:

```bash
# Make changes to any component
cd ~/stoffel-dev/Stoffel
# ... make your changes ...

# Rebuild and reinstall
cargo build --release
cp target/release/stoffel ~/.local/bin/

# Test your changes
stoffel --version
```

This manual installation process gives you full control over the Stoffel components and allows you to track the latest development progress.

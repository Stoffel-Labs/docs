# Introduction

> **⚠️ Work in Progress Notice**
>
> This documentation is actively being developed and is subject to frequent changes.
> Some sections may be incomplete or pending review.

## About Stoffel

Stoffel is a comprehensive framework for building privacy-preserving applications using secure Multi-Party Computation (MPC). It provides a complete toolchain that enables developers to create, compile, and deploy MPC applications without requiring deep cryptographic expertise.

## The Stoffel Ecosystem

Stoffel consists of several integrated components that work together to provide a seamless development experience:

### Core Components

- **Stoffel CLI**: A comprehensive command-line interface for project management, compilation, development, and deployment
- **StoffelLang**: A modern programming language with syntax inspired by Rust, Python, and JavaScript, designed specifically for MPC applications
- **StoffelVM**: A register-based virtual machine optimized for multiparty computation with support for both clear and secret values
- **MPC Protocols**: Rust implementation of secure multiparty computation protocols, including HoneyBadger MPC
- **Python SDK**: High-level Python interface for integrating Stoffel into existing applications

### Key Features

- **Modern Development Experience**: Project templates, hot-reloading development server, and comprehensive CLI tools
- **Multiple Language Support**: Templates and SDKs for Python, Rust, TypeScript, and Solidity integration
- **Rich Type System**: Support for integers, floats, strings, booleans, arrays, objects, and closures
- **VM Architecture**: Register-based design with separate clear/secret registers for efficient MPC operations
- **Production Ready**: Built-in deployment tools with support for TEE and cloud environments

## Current Status

The Stoffel ecosystem is under active development:

- ✅ **StoffelVM**: Core virtual machine with instruction set and runtime (functional with quirks)
- ✅ **Stoffel CLI**: Comprehensive project management and build tools
- ✅ **StoffelLang**: Compiler with VM-compatible binary generation
- ✅ **Python SDK**: Clean API with proper separation of concerns
- 🚧 **MPC Integration**: Full MPC protocol integration (in progress)
- 🚧 **Production Deployment**: TEE and cloud deployment features

## Getting Started

The best way to start with Stoffel is to:

1. [Install the Stoffel CLI](./getting-started/installation.md)
2. [Create your first MPC project](./getting-started/first-project.md)
3. [Explore the ecosystem](./introduction/ecosystem.md)

## Documentation Structure

This documentation is organized to guide you through the Stoffel ecosystem:

- **[Getting Started](./getting-started/installation.md)**: Installation, quick start, and first project
- **[Stoffel CLI](./cli/overview.md)**: Comprehensive guide to the command-line interface
- **[StoffelLang](./stoffel-lang/overview.md)**: Programming language syntax and compilation
- **[StoffelVM](./stoffel-vm/overview.md)**: Virtual machine architecture and usage
- **[Python SDK](./python-sdk/overview.md)**: Python integration and API reference
- **[Architecture](./architecture/system.md)**: System design and technical details
- **[Development](./development/contributing.md)**: Contributing and building from source

# StoffelLang Overview

StoffelLang is a modern programming language designed specifically for secure Multi-Party Computation (MPC) applications. With syntax inspired by Rust, Python, and JavaScript, it provides a familiar development experience while offering powerful features for privacy-preserving computation.

## Design Goals

StoffelLang is designed with the following principles:

- **Familiar Syntax**: Draws from popular languages to reduce learning curve
- **Type Safety**: Strong static typing with type inference for reliability
- **MPC Native**: Built-in support for secret and public data distinctions
- **Performance**: Compiles to efficient StoffelVM bytecode
- **Developer Experience**: Clear error messages and tooling integration

## Key Features

### Modern Language Features

- **Static Typing**: Strong type system with inference to catch errors early
- **Pattern Matching**: Powerful pattern matching for control flow
- **Closures**: First-class functions with lexical scoping
- **Memory Safety**: Automatic memory management without garbage collection overhead
- **Generics**: Parametric polymorphism for reusable code

### MPC-Specific Features

- **Secret Types**: Native support for `secret` type annotations
- **Reveal Operations**: Explicit operations for transitioning from secret to public
- **Protocol Agnostic**: Works with different MPC protocol backends
- **Optimized Compilation**: Generates efficient MPC-aware bytecode

## Syntax Overview

### Basic Syntax

```
# Variables and types
let x: int64 = 42
let y = 3.14  # Type inference
let name = "Stoffel"
let is_active = true

# Functions
proc add(a: int64, b: int64): int64 =
  return a + b

# Control flow
if x > 0:
  print("Positive")
else:
  print("Non-positive")

# Loops
for i in 0..10:
  print("Count: " + $i)
```

### MPC-Specific Syntax

```
# Secret types
proc secure_add(a: secret int64, b: secret int64): secret int64 =
  return a + b

# Mixed computation
proc threshold_check(secret_value: secret int64, threshold: int64): secret bool =
  return secret_value > threshold

# Reveal operations (conceptual - actual implementation varies)
proc main() =
  let secret_sum = secure_add(25, 17)
  print("Computation completed securely")
```

### Advanced Features

```
# Type definitions
type Person = object
  name: string
  age: int64
  is_secret: bool

# Object creation
let alice = Person(
  name: "Alice",
  age: 25,
  is_secret: false
)

# Enum definitions (planned)
type Status = enum
  Active
  Inactive
  Pending
```

## Type System

### Primitive Types

- **`int64`**: 64-bit signed integers (primary integer type)
- **`bool`**: Boolean values (`true`, `false`)
- **`string`**: UTF-8 strings
- **`nil`**: Null/empty value

### Collection Types

- **Objects**: Structured data with named fields
- **Enums**: Enumerated types with named variants
- **Lists**: Dynamic arrays (planned)
- **Tuples**: Fixed-size heterogeneous collections (planned)

### Secret Types

Any type can be made secret by prefixing with `secret`:

```
let public_value: int64 = 42
let secret_value: secret int64 = 42
let secret_name: secret string = "Alice"
```

### Function Types

```
# Function definitions
proc add(a: int64, b: int64): int64 =
  return a + b

proc multiply(x: int64, y: int64): int64 =
  return x * y

# Functions can call other functions
proc calculate(a: int64, b: int64): int64 =
  let sum = add(a, b)
  let product = multiply(a, b)
  return sum + product
```

## Compilation Process

StoffelLang follows a multi-stage compilation process:

```
Source (.stfl) → Lexer → Parser → Type Checker → Code Generator → Bytecode (.stfbin)
```

### Compilation Stages

1. **Lexical Analysis**: Tokenizes source code
2. **Parsing**: Builds Abstract Syntax Tree (AST)
3. **Type Checking**: Verifies type correctness and infers types
4. **Optimization**: Applies various optimization passes
5. **Code Generation**: Generates StoffelVM bytecode

### Optimization Levels

```bash
# Different optimization levels
stoffel compile source.stfl -O0    # No optimization (debug)
stoffel compile source.stfl -O1    # Basic optimization
stoffel compile source.stfl -O2    # Standard optimization
stoffel compile source.stfl -O3    # Maximum optimization
```

## Integration with StoffelVM

StoffelLang compiles to StoffelVM bytecode, which includes:

- **Rich Type Information**: Preserves type metadata for runtime
- **Function Definitions**: Complete function metadata and instructions
- **Constant Pools**: Efficient storage for literals and constants
- **Debug Information**: Line numbers and variable names for debugging

### Binary Format

The compiler generates `.stfbin` files that contain:

```
┌─────────────────┐
│   File Header   │
├─────────────────┤
│  Type Metadata  │
├─────────────────┤
│   Constant Pool │
├─────────────────┤
│   Function Defs │
├─────────────────┤
│   Bytecode      │
├─────────────────┤
│  Debug Info     │
└─────────────────┘
```

## Development Tools

### Compiler CLI

```bash
# Basic compilation
stoffel compile source.stfl

# Generate VM-compatible binary
stoffel compile source.stfl --binary

# Enable optimizations
stoffel compile source.stfl --binary -O2

# Print intermediate representations
stoffel compile source.stfl --print-ir
```

### Integration with Stoffel CLI

The StoffelLang compiler is integrated with the main Stoffel CLI:

```bash
# Compile via Stoffel CLI
stoffel compile src/main.stfl

# Compile with optimizations
stoffel compile src/main.stfl --binary -O3

# Development workflow
stoffel compile src/main.stfl --binary --output app.stfbin
stoffel-run app.stfbin main
```

## Examples

### Hello World

```
proc main() =
  print("Hello, world!")
```

### Secure Addition

```
proc secure_add(a: secret int64, b: secret int64): secret int64 =
  return a + b

proc main() =
  let result = secure_add(25, 17)
  print("Secure addition completed")
```

### Complex Data Structures

```
type Person = object
  name: string
  age: secret int64
  email: string

proc process_person(person: Person): bool =
  # Note: Age comparison would need special MPC operations
  return true  # Simplified for example

proc main() =
  let alice = Person(
    name: "Alice",
    age: secret(25),
    email: "alice@example.com"
  )

  let is_adult = process_person(alice)
  print("Person processed: " + $is_adult)
```

### Basic Computation

```
proc calculate_total(base: int64, multiplier: int64): int64 =
  return base * multiplier

proc main() =
  let base_value: int64 = 100
  let factor: int64 = 3
  let total = calculate_total(base_value, factor)
  print("Total: " + $total)
```

## Future Features

Planned enhancements for StoffelLang:

- **Pattern Matching**: Powerful pattern matching for complex data
- **Generics**: Parametric polymorphism for reusable code
- **Async/Await**: Asynchronous programming support
- **Macros**: Compile-time code generation
- **Package System**: Module imports and dependency management
- **Standard Library**: Comprehensive built-in functions and types

## Language Server

A Language Server Protocol (LSP) implementation is planned to provide:

- **Syntax Highlighting**: Rich syntax highlighting in editors
- **Error Reporting**: Real-time error checking and suggestions
- **Auto-completion**: Intelligent code completion
- **Go-to Definition**: Navigate to symbol definitions
- **Refactoring**: Automated code refactoring tools

## Next Steps

To learn more about StoffelLang:

- **[Syntax and Examples](./syntax.md)**: Detailed syntax guide with examples
- **[Compilation](./compilation.md)**: Understanding the compilation process
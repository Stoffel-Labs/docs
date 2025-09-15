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

```javascript
// Variables and types
let x: i32 = 42;
let y = 3.14;  // Type inference
let name = "Stoffel";
let is_active = true;

// Functions
fn add(a: i32, b: i32) -> i32 {
    return a + b;
}

// Control flow
if x > 0 {
    println("Positive");
} else {
    println("Non-positive");
}

// Loops
for i in 0..10 {
    println("Count: {}", i);
}
```

### MPC-Specific Syntax

```javascript
// Secret types
fn secure_add(a: secret i32, b: secret i32) -> secret i32 {
    return a + b;
}

// Mixed computation
fn threshold_check(secret_value: secret i32, threshold: i32) -> secret bool {
    return secret_value > threshold;
}

// Reveal operations
fn main() {
    let secret_sum = secure_add(25, 17);
    let public_result = reveal(secret_sum);
    println("Result: {}", public_result);
}
```

### Advanced Features

```javascript
// Closures
let multiplier = |x: i32| -> i32 { x * 2 };
let result = multiplier(21);

// Generics (planned)
fn identity<T>(value: T) -> T {
    return value;
}

// Pattern matching (planned)
match value {
    Some(x) => println("Value: {}", x),
    None => println("No value"),
}
```

## Type System

### Primitive Types

- **`i32`, `i64`**: Signed integers
- **`u32`, `u64`**: Unsigned integers
- **`f32`, `f64`**: Floating-point numbers
- **`bool`**: Boolean values
- **`string`**: UTF-8 strings

### Collection Types

- **Arrays**: `[T; N]` for fixed-size, `Vec<T>` for dynamic
- **Objects**: Key-value mappings similar to JavaScript objects
- **Tuples**: `(T1, T2, ...)` for heterogeneous data

### Secret Types

Any type can be made secret by prefixing with `secret`:

```javascript
let public_value: i32 = 42;
let secret_value: secret i32 = 42;
let secret_array: secret [i32; 10] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
```

### Function Types

```javascript
// Function types
type BinaryOp = fn(i32, i32) -> i32;
let add: BinaryOp = |a, b| a + b;

// Closures with captured variables
fn make_adder(x: i32) -> fn(i32) -> i32 {
    return |y| x + y;
}
```

## Compilation Process

StoffelLang follows a multi-stage compilation process:

```
Source (.stfl) → Lexer → Parser → Type Checker → Code Generator → Bytecode (.stfb)
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
stoffellang -O0 source.stfl    # No optimization (debug)
stoffellang -O1 source.stfl    # Basic optimization
stoffellang -O2 source.stfl    # Standard optimization
stoffellang -O3 source.stfl    # Maximum optimization
```

## Integration with StoffelVM

StoffelLang compiles to StoffelVM bytecode, which includes:

- **Rich Type Information**: Preserves type metadata for runtime
- **Function Definitions**: Complete function metadata and instructions
- **Constant Pools**: Efficient storage for literals and constants
- **Debug Information**: Line numbers and variable names for debugging

### Binary Format

The compiler generates `.stfb` files that contain:

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
stoffellang source.stfl

# Generate VM-compatible binary
stoffellang -b source.stfl

# Enable optimizations
stoffellang -O2 -b source.stfl

# Print intermediate representations
stoffellang --print-ir source.stfl
```

### Integration with Stoffel CLI

The StoffelLang compiler is integrated with the main Stoffel CLI:

```bash
# Compile via Stoffel CLI
stoffel compile src/main.stfl

# Compile with optimizations
stoffel compile --binary -O3

# Watch mode for development
stoffel dev
```

## Examples

### Hello World

```javascript
fn main() {
    println("Hello, world!");
}
```

### Secure Addition

```javascript
fn secure_add(a: secret i32, b: secret i32) -> secret i32 {
    return a + b;
}

fn main() {
    let result = secure_add(25, 17);
    let revealed = reveal(result);
    println("Secure addition result: {}", revealed);
}
```

### Complex Data Structures

```javascript
struct Person {
    name: string,
    age: secret i32,
    email: string,
}

fn process_person(person: Person) -> secret bool {
    return person.age >= 18;
}

fn main() {
    let alice = Person {
        name: "Alice",
        age: secret(25),
        email: "alice@example.com",
    };

    let is_adult = process_person(alice);
    let result = reveal(is_adult);
    println("Is adult: {}", result);
}
```

### Arrays and Iteration

```javascript
fn sum_array(arr: secret [i32; 5]) -> secret i32 {
    let sum = secret(0);
    for i in 0..5 {
        sum = sum + arr[i];
    }
    return sum;
}

fn main() {
    let numbers = secret([1, 2, 3, 4, 5]);
    let total = sum_array(numbers);
    let result = reveal(total);
    println("Sum: {}", result);
}
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
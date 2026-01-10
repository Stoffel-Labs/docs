# Compilation

This page explains the StoffelLang compilation process, from source code to executable bytecode, including optimization techniques and debugging capabilities.

## Overview

StoffelLang uses a multi-stage compilation pipeline that transforms human-readable source code into efficient bytecode for the StoffelVM. The compiler is designed to provide excellent error messages, strong type checking, and optimizations specific to MPC computations.

## Compilation Pipeline

### Stage 1: Lexical Analysis

The lexer tokenizes the source code, breaking it into meaningful tokens:

```
Source: let x: int64 = 42
Tokens: [LET, IDENTIFIER("x"), COLON, IDENTIFIER("int64"), ASSIGN, INT_LITERAL(42)]
```

**Key Features:**
- **Indentation-based**: Uses 2-space indentation (tabs not allowed)
- **Unicode support**: Full UTF-8 string and identifier support
- **Error recovery**: Continues parsing after errors to find more issues

### Stage 2: Parsing

The parser builds an Abstract Syntax Tree (AST) from the token stream:

```
AST Node: VariableDeclaration {
  name: "x",
  type_annotation: Some(Identifier("int64")),
  value: Some(Literal(Int(42))),
  is_mutable: false,
  is_secret: false,
  location: SourceLocation { line: 1, column: 1 }
}
```

**Parser Features:**
- **Recursive descent**: Predictable parsing with clear error messages
- **Location tracking**: Every AST node includes source location
- **Error recovery**: Attempts to continue parsing after syntax errors

### Stage 3: Semantic Analysis

The semantic analyzer performs type checking and builds the symbol table:

**Type Checking:**
```
# This would produce a type error
let name: string = 42  # Error: Cannot assign int64 to string

# This works correctly
let age: int64 = 42    # OK: Types match
```

**Symbol Resolution:**
```
def add(a: int64, b: int64) -> int64:
  return a + b  # Resolves 'a' and 'b' to parameters

let result = add(10, 20)  # Resolves 'add' to function definition
```

### Stage 4: Code Generation

Generates StoffelVM bytecode from the validated AST:

```
StoffelLang:           Bytecode:
let x: int64 = 42      LDI R0, 42
                      STORE x, R0

def add(a: int64, b: int64) -> int64:   FUNCTION add:
  return a + b                            LOAD R0, a
                                          LOAD R1, b
                                          ADD R0, R0, R1
                                          RET R0
```

## Using the Compiler

### Basic Compilation

```bash
# Compile a single file
stoffel compile src/main.stfl

# Compile to VM-compatible binary
stoffel compile src/main.stfl --binary --output program.stfbin

# Compile all files in src/
stoffel compile
```

### Compilation Options

#### Optimization Levels

```bash
# No optimization (fastest compilation, good for debugging)
stoffel compile src/main.stfl -O0

# Basic optimizations (balanced)
stoffel compile src/main.stfl -O1

# Standard optimizations (recommended for production)
stoffel compile src/main.stfl -O2

# Maximum optimizations (slowest compilation, best performance)
stoffel compile src/main.stfl -O3
```

#### Output Formats

```bash
# Default bytecode format
stoffel compile src/main.stfl

# VM-compatible binary (for execution)
stoffel compile src/main.stfl --binary --output app.stfbin

# Specify custom output location
stoffel compile src/main.stfl --output custom/path/program.stfbin
```

#### Debug Information

```bash
# Include debug symbols
stoffel compile src/main.stfl --debug

# Print intermediate representations
stoffel compile src/main.stfl --print-ir

# Verbose compilation output
stoffel compile src/main.stfl --verbose
```

## Optimization Techniques

### Constant Folding

The compiler evaluates constant expressions at compile time:

```
# Source code
let result = 2 + 3 * 4

# Optimized to
let result = 14
```

### Dead Code Elimination

Removes unreachable code:

```
# Source code
def example(flag: bool) -> nil:
  if true:
    print("Always executed")
  else:
    print("Never executed")  # Removed by optimizer

# Optimized to
def example(flag: bool) -> nil:
  print("Always executed")
```

### Function Inlining

Small functions may be inlined at call sites:

```
# Source code
def square(x: int64) -> int64:
  return x * x

let result = square(5)

# May be optimized to
let result = 5 * 5
```

### Secret Operation Optimization

Special optimizations for MPC operations:

```
# Source code
let a: secret int64 = 10
let b: secret int64 = 20
let sum = a + b
let product = a * b

# Compiler may batch secret operations for efficiency
```

## Error Handling

### Syntax Errors

Clear error messages with source locations:

```
Error: Unexpected token 'let'
  --> src/main.stfl:5:3
   |
 5 |   let x = 42
   |   ^^^ Expected expression, found 'let'
   |
Help: Variable declarations must be at the top level of a block
```

### Type Errors

Detailed type mismatch information:

```
Error: Type mismatch in assignment
  --> src/main.stfl:8:12
   |
 8 | let name: string = 42
   |           ------   ^^ Expected 'string', found 'int64'
   |           |
   |           Variable declared as 'string' here
   |
Help: Convert the integer to string: "42" or $42
```

### Semantic Errors

Context-aware error messages:

```
Error: Cannot find value 'undefined_var' in this scope
  --> src/main.stfl:12:15
   |
12 |   return undefined_var + 10
   |                ^^^^^^^^^^^^
   |
Help: Did you mean 'defined_var'? (defined at line 3)
```

## Intermediate Representations

### Viewing IR with --print-ir

```bash
stoffel compile src/main.stfl --print-ir
```

**Output includes:**
1. **Tokens**: Lexical analysis output
2. **AST**: Parsed syntax tree
3. **Type Information**: Resolved types and symbols
4. **Bytecode**: Generated VM instructions

### Example IR Output

```
=== TOKENS ===
LET(1:1) IDENTIFIER("x", 1:5) COLON(1:6) IDENTIFIER("int64", 1:8) ASSIGN(1:14) INT_LITERAL(42, 1:16)

=== AST ===
VariableDeclaration {
  name: "x",
  type_annotation: Some(TypeRef("int64")),
  value: Some(IntLiteral(42)),
  is_mutable: false,
  location: SourceLocation(1:1)
}

=== BYTECODE ===
Constants:
  0: Int(42)

Instructions:
  0000: LDC R0, 0     ; Load constant 42
  0001: STORE x, R0   ; Store in variable x
```

## Binary Format

### File Structure

StoffelLang produces `.stfbin` files with the following structure:

```
┌─────────────────┐
│   Magic Number  │  4 bytes: "STFL"
├─────────────────┤
│   Version       │  4 bytes: Format version
├─────────────────┤
│   Metadata      │  Variable: Type information
├─────────────────┤
│   Constants     │  Variable: Constant pool
├─────────────────┤
│   Functions     │  Variable: Function definitions
├─────────────────┤
│   Instructions  │  Variable: Bytecode instructions
├─────────────────┤
│   Debug Info    │  Variable: Source locations
└─────────────────┘
```

### Binary Inspection

```bash
# Disassemble a compiled binary
stoffel compile program.stfbin --disassemble

# Output shows human-readable bytecode
FUNCTION main:
  Constants: [Int(42), String("Hello")]
  Instructions:
    0000: LDC R0, 0      ; Load 42
    0001: LDC R1, 1      ; Load "Hello"
    0002: CALL print     ; Call print function
    0003: RET R0         ; Return
```

## Compilation Workflow

### Single File Compilation

```bash
# 1. Compile source to binary
stoffel compile src/main.stfl --binary --output app.stfbin

# 2. Run the compiled program
stoffel-run app.stfbin main

# 3. Debug if needed
stoffel-run app.stfbin main --trace-instr
```

### Multi-File Projects

```bash
# 1. Compile all files
stoffel compile

# 2. The compiler automatically handles dependencies
# Files are compiled in dependency order

# 3. Single binary output contains all functions
```

### Development Workflow

```bash
# 1. Write code
# edit src/main.stfl

# 2. Quick compile check
stoffel compile src/main.stfl

# 3. Full compile and test
stoffel compile src/main.stfl --binary --output test.stfbin
stoffel-run test.stfbin main

# 4. Debug compilation issues
stoffel compile src/main.stfl --print-ir

# 5. Production build
stoffel compile src/main.stfl --binary -O3 --output production.stfbin
```

## Performance Considerations

### Compilation Speed

| Optimization Level | Compile Time | Runtime Performance |
|-------------------|--------------|-------------------|
| -O0               | Fastest      | Basic             |
| -O1               | Fast         | Good              |
| -O2               | Medium       | Better            |
| -O3               | Slowest      | Best              |

### Memory Usage

- **Compiler memory**: Scales with source code size and complexity
- **Binary size**: Optimizations can reduce final binary size
- **Runtime memory**: Efficient bytecode reduces VM memory usage

### Secret Type Optimization

Special considerations for MPC operations:

```
# Expensive: Many individual secret operations
def inefficient(a: secret int64, b: secret int64) -> secret int64:
  let temp1 = a + 1
  let temp2 = b + 1
  let temp3 = temp1 + temp2
  return temp3 + 1

# Better: Batched operations where possible
def efficient(a: secret int64, b: secret int64) -> secret int64:
  return a + b + 2  # Compiler can optimize this
```

## Troubleshooting

### Common Compilation Errors

**"Tabs are not allowed"**
```bash
# Fix: Use 2 spaces instead of tabs
# Bad:
	let x = 42
# Good:
  let x = 42
```

**"Indentation error"**
```bash
# Fix: Consistent 2-space indentation
def example() -> nil:
  if true:
    print("Correct indentation")
```

**"Type mismatch"**
```bash
# Fix: Ensure types match
let age: int64 = 25      # Correct
let name: string = "Bob" # Correct
# let wrong: string = 42  # Error
```

### Debugging Tips

1. **Use --print-ir** to see what the compiler generated
2. **Start with -O0** for debugging, optimize later
3. **Check types explicitly** rather than relying on inference
4. **Use --verbose** to see detailed compilation steps

### Performance Issues

1. **Profile with --trace-instr** during execution
2. **Try different optimization levels**
3. **Review generated bytecode** with --disassemble
4. **Minimize secret operations** where possible

## Integration with Development Tools

### Editor Integration

```bash
# Generate compilation database for editors
stoffel compile --export-compile-commands

# This creates compile_commands.json for IDE integration
```

### Build Systems

```bash
# Makefile integration
%.stfbin: %.stfl
	stoffel compile $< --binary --output $@

# Used as:
# make program.stfbin
```

### Continuous Integration

```bash
#!/bin/bash
# CI script for StoffelLang projects

# Compile all files
stoffel compile

# Compile with different optimization levels
stoffel compile --binary -O0 --output debug.stfbin
stoffel compile --binary -O3 --output release.stfbin

# Run basic tests
stoffel-run debug.stfbin main
```

## Advanced Topics

### Cross-Compilation

Currently, StoffelLang generates platform-independent bytecode that runs on any StoffelVM instance.

### Linking (Future)

Planned support for linking multiple compiled modules:

```bash
# Compile library
stoffel compile --lib src/math.stfl --output math.stflib

# Link with main program
stoffel compile src/main.stfl --link math.stflib --output app.stfbin
```

### Plugin Architecture (Future)

Support for compiler plugins to extend functionality:

```bash
# Custom optimization passes
stoffel compile --plugin my_optimizer.so src/main.stfl

# Custom code generators
stoffel compile --target wasm --plugin wasm_gen.so src/main.stfl
```

This compilation guide provides comprehensive information about building StoffelLang programs and optimizing them for the StoffelVM runtime environment.
# Using the VM

This guide covers how to run compiled StoffelLang programs using StoffelVM, including command-line options, debugging techniques, and integration with MPC protocols.

## Running Programs

### Basic Execution

After compiling a StoffelLang program to bytecode, use `stoffel-run` to execute it:

```bash
# Basic execution
stoffel-run program.stfbin main

# Specify a different entry function
stoffel-run program.stfbin my_entry_point
```

**Parameters:**
- `program.stfbin`: Path to the compiled bytecode file
- `main`: Name of the entry function to execute (optional, defaults to `main`)

### Output

A successful execution returns the program's result:

```bash
$ stoffel-run fibonacci.stfbin main
Program returned: 55
```

For programs that return `nil`:

```bash
$ stoffel-run hello.stfbin main
Hello, World!
Program returned: Unit
```

## Command-Line Flags

### Debugging Flags

StoffelVM provides detailed tracing for debugging program execution:

| Flag | Description |
|------|-------------|
| `--trace-instr` | Trace instructions before and after execution |
| `--trace-regs` | Trace register read and write operations |
| `--trace-stack` | Trace function calls and stack operations |

### Instruction Tracing

```bash
stoffel-run program.stfbin main --trace-instr
```

**Example output:**
```
[INSTR] 0x0000: LDI r0, 42
[INSTR] 0x0004: LDI r1, 10
[INSTR] 0x0008: ADD r2, r0, r1
[INSTR] 0x000c: RET r2
```

This shows:
- Instruction address
- Opcode and operands
- Register assignments

### Register Tracing

```bash
stoffel-run program.stfbin main --trace-regs
```

**Example output:**
```
[REG] WRITE r0 = 42
[REG] WRITE r1 = 10
[REG] READ r0 -> 42
[REG] READ r1 -> 10
[REG] WRITE r2 = 52
```

This shows:
- Register reads and writes
- Values being stored and retrieved
- Clear vs secret register operations

### Stack Tracing

```bash
stoffel-run program.stfbin main --trace-stack
```

**Example output:**
```
[STACK] CALL fibonacci(10) at 0x0020
[STACK] PUSH frame: locals=2, args=1
[STACK] CALL fibonacci(9) at 0x0020
[STACK] PUSH frame: locals=2, args=1
...
[STACK] POP frame, returning 55
[STACK] RET to 0x0024
```

This shows:
- Function call entries and exits
- Stack frame allocation
- Return addresses and values

### Combined Tracing

For comprehensive debugging, combine multiple flags:

```bash
stoffel-run program.stfbin main --trace-instr --trace-regs --trace-stack
```

## Bytecode File Format

### File Extensions

| Extension | Description |
|-----------|-------------|
| `.stfbin` | Binary bytecode format (recommended) |
| `.stfb` | Alternative binary extension |
| `.bc` | Text-based bytecode (for debugging) |

### Binary Structure

The `.stfbin` file contains:

1. **Header**: Magic bytes, version, metadata
2. **Constants pool**: Literal values and strings
3. **Main chunk**: Entry point bytecode
4. **Function chunks**: Compiled function bodies

## Execution Modes

### Local Execution

For development and testing without MPC:

```bash
# Single-party execution (no network)
stoffel-run program.stfbin main
```

In local mode:
- Secret values are computed directly (not distributed)
- Useful for logic testing before MPC deployment
- Full debugging support available

### MPC Execution

For distributed secure computation:

```bash
# Using the Rust SDK
cargo run --example honeybadger_mpc_demo
```

In MPC mode:
- Values are secret-shared across parties
- HoneyBadger protocol handles Byzantine fault tolerance
- Requires network configuration (see [Rust SDK](../rust-sdk/overview.md))

## Integration with MPC Protocols

### HoneyBadger Integration

StoffelVM integrates with the HoneyBadger MPC protocol for secure multi-party computation:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Party 1   │     │   Party 2   │     │   Party 3   │
│  StoffelVM  │◄───►│  StoffelVM  │◄───►│  StoffelVM  │
│   Instance  │     │   Instance  │     │   Instance  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                    HoneyBadger Protocol
                    (Byzantine Fault Tolerant)
```

### Configuration Requirements

For MPC execution, all parties must agree on:

| Parameter | Constraint | Example |
|-----------|------------|---------|
| `n_parties` | Number of compute nodes | 5 |
| `threshold` | Max faulty parties | 1 |
| `instance_id` | Unique computation ID | 12345 |

**Validation rule**: `n_parties >= 3 * threshold + 1`

Valid configurations:
- 4 parties, threshold 1: `4 >= 4` ✓
- 5 parties, threshold 1: `5 >= 4` ✓ (recommended minimum)
- 7 parties, threshold 2: `7 >= 7` ✓

### ClientStore Integration

When running with MPC, the VM's `ClientStore` is populated with client shares:

```python
main main() -> nil:
    # These calls retrieve actual shares from MPC clients
    secret var input1 = ClientStore.take_share(0, 0)
    secret var input2 = ClientStore.take_share(1, 0)

    # Computation happens on shares
    secret var result = input1 + input2
```

## Error Handling

### Common Errors

**"Error loading binary"**
```
Error: Failed to load binary: No such file or directory
```
- Verify the file path is correct
- Ensure the file was compiled successfully

**"Function not found"**
```
Error: Entry function 'main' not found in program
```
- Check the entry function name matches what's in the source
- Use `--trace-instr` to see available functions

**"Stack overflow"**
```
Error: Stack overflow: maximum depth exceeded
```
- Check for infinite recursion
- Consider iterative alternatives for deep recursion

**"Type mismatch"**
```
Error: Type mismatch in register operation
```
- Verify operand types match expected types
- Check for mixing clear and secret values incorrectly

### Debugging Workflow

1. **Start with instruction tracing**:
   ```bash
   stoffel-run program.stfbin main --trace-instr
   ```

2. **Add register tracing for value issues**:
   ```bash
   stoffel-run program.stfbin main --trace-instr --trace-regs
   ```

3. **Add stack tracing for call issues**:
   ```bash
   stoffel-run program.stfbin main --trace-instr --trace-stack
   ```

## Performance Considerations

### Register Architecture

StoffelVM uses a dual-register architecture:

- **Clear registers**: Fast operations on public values
- **Secret registers**: MPC-protected operations on private values

Mixing clear and secret values appropriately can improve performance.

### Optimization Levels

When compiling with StoffelLang, use optimization flags:

```bash
# No optimization (fastest compile, slowest run)
stoffellang -O0 program.stfl -b

# Basic optimization
stoffellang -O1 program.stfl -b

# Standard optimization (recommended)
stoffellang -O2 program.stfl -b

# Aggressive optimization (longest compile, fastest run)
stoffellang -O3 program.stfl -b
```

## Examples

### Simple Arithmetic

```bash
# Compile
stoffellang arithmetic.stfl -b

# Run
stoffel-run arithmetic.stfbin main
```

### Fibonacci with Debugging

```bash
# Compile with debug info
stoffellang fibonacci.stfl -b --print-ir

# Run with full tracing
stoffel-run fibonacci.stfbin main --trace-instr --trace-regs --trace-stack
```

### MPC Integration Test

```bash
# Build the Rust SDK example
cd SDKs/stoffel-rust-sdk
cargo build --example honeybadger_mpc_demo

# Run the MPC demo (starts 5 parties locally)
cargo run --example honeybadger_mpc_demo
```

## Next Steps

- [Built-in Functions](./builtins.md): Reference for available builtins
- [Instructions](./instructions.md): Complete instruction set documentation
- [Rust SDK](../rust-sdk/overview.md): Integrate with Rust applications
- [MPC Protocols](../mpc-protocols/overview.md): Understand the underlying cryptography

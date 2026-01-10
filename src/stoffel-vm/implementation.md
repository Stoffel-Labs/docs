# StoffelVM Overview

StoffelVM is a register-based virtual machine specifically designed and optimized for secure Multi-Party Computation (MPC). It provides a flexible and efficient foundation for executing MPC protocols while maintaining protocol agnosticism.

## Key Features

### Register-Based Architecture
Unlike stack-based VMs, StoffelVM uses a register-based design that enables:
- **Easy Optimization**: Direct mapping to physical hardware registers
- **Efficient Compilation**: Cleaner code generation from high-level languages
- **MPC Optimization**: Separate handling of clear and secret values

### Rich Type System
StoffelVM supports a comprehensive set of value types:

- **Primitives**: `i64` integers, fixed-point floats, booleans, strings
- **Collections**: Arrays and objects with dynamic sizing
- **Functions**: Closures with true lexical scoping and upvalue capture
- **Foreign Objects**: FFI integration with host language objects
- **Unit Type**: Void/null values for control flow

### MPC Integration
The VM is designed with MPC in mind:
- **Clear/Secret Separation**: Distinct register spaces for public and private data
- **Protocol Agnosticism**: Works with different MPC protocol implementations
- **Efficient Sharing**: Optimized handling of secret-shared values

## Current Status

> 🚧 **Development Status**
>
> StoffelVM is currently functional with some quirks. The core VM operations work well, but full MPC functionality is still in development.

**Working Features:**
- ✅ Complete instruction set implementation
- ✅ Register management and memory operations
- ✅ Arithmetic and bitwise operations
- ✅ Control flow (jumps, calls, returns)
- ✅ Object and array manipulation
- ✅ Closure system with lexical scoping
- ✅ Foreign function interface (FFI)
- ✅ Built-in standard library functions

**In Development:**
- 🚧 Full MPC protocol integration
- 🚧 Automatic memory management/garbage collection
- 🚧 Exception handling system
- 🚧 Dynamic library loading/unloading
- 🚧 Tail call optimization

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    StoffelVM                            │
├─────────────────────┬───────────────────────────────────┤
│   Clear Registers   │        Secret Registers          │
│   (Public Data)     │       (Private/Shared Data)      │
├─────────────────────┼───────────────────────────────────┤
│              Instruction Processor                     │
├─────────────────────────────────────────────────────────┤
│                 Memory Management                      │
├─────────────────────┬───────────────────────────────────┤
│   Object Store      │         Array Store             │
├─────────────────────┼───────────────────────────────────┤
│   Closure System    │      Foreign Objects            │
├─────────────────────┴───────────────────────────────────┤
│                    Hook System                         │
│              (Debugging & Protocol Integration)        │
└─────────────────────────────────────────────────────────┘
```

## Value Types

### Primitive Types

```rust
Value::I64(i64)           // 64-bit signed integers
Value::I32(i32)           // 32-bit signed integers
Value::I16(i16)           // 16-bit signed integers
Value::I8(i8)             // 8-bit signed integers
Value::U8(u8)             // 8-bit unsigned integers
Value::U16(u16)           // 16-bit unsigned integers
Value::U32(u32)           // 32-bit unsigned integers
Value::U64(u64)           // 64-bit unsigned integers
Value::Float(F64)         // 64-bit floating point (F64 wrapper)
Value::Bool(bool)         // Boolean values
Value::String(String)     // UTF-8 strings
Value::Unit               // Unit/void type
```

### Complex Types

```rust
Value::Object(usize)      // Object reference (key-value pairs)
Value::Array(usize)       // Array reference (indexed values)
Value::Closure(Arc<Closure>) // Function closure with captured variables
Value::Foreign(usize)     // Foreign object from host language
Value::Share(ShareType, Vec<u8>) // Secret shared value for MPC
```

## Instruction Set

### Memory Operations

```
LD(dest_reg, stack_offset)    // Load from stack to register
LDI(dest_reg, value)          // Load immediate value
MOV(dest_reg, src_reg)        // Move between registers
PUSHARG(reg)                  // Push register as function argument
```

### Arithmetic Operations

```
ADD(dest, src1, src2)         // Addition
SUB(dest, src1, src2)         // Subtraction
MUL(dest, src1, src2)         // Multiplication
DIV(dest, src1, src2)         // Division
MOD(dest, src1, src2)         // Modulo
```

### Bitwise Operations

```
AND(dest, src1, src2)         // Bitwise AND
OR(dest, src1, src2)          // Bitwise OR
XOR(dest, src1, src2)         // Bitwise XOR
NOT(dest, src)                // Bitwise NOT
SHL(dest, src, amount)        // Shift left
SHR(dest, src, amount)        // Shift right
```

### Control Flow

```
JMP(label)                    // Unconditional jump
JMPEQ(label)                  // Jump if equal
JMPNEQ(label)                 // Jump if not equal
CMP(reg1, reg2)               // Compare registers
CALL(function_name)           // Function call
RET(reg)                      // Return with value
```

## Usage Patterns

### Embedding in Applications

The VM is designed to be embedded in larger applications:

```rust
use stoffel_vm::core_vm::VirtualMachine;
use stoffel_vm::functions::VMFunction;
use stoffel_vm::instructions::Instruction;
use stoffel_vm::core_types::Value;

fn main() -> Result<(), String> {
    let vm = VirtualMachine::new();

    // Register a function
    let hello_world = VMFunction {
        name: "hello_world".to_string(),
        parameters: vec![],
        upvalues: vec![],
        parent: None,
        register_count: 1,
        instructions: vec![
            Instruction::LDI(0, Value::String("Hello, World!".to_string())),
            Instruction::PUSHARG(0),
            Instruction::CALL("print".to_string()),
            Instruction::RET(0),
        ],
        labels: HashMap::new(),
    };

    vm.register_function(hello_world);

    // Execute the function
    let result = vm.execute("hello_world")?;
    println!("Result: {:?}", result);

    Ok(())
}
```

### CLI Usage

The VM can also be used via the CLI to run compiled programs:

```bash
# Build the CLI
cargo build --release -p stoffel-vm

# Run a compiled program
./target/release/stoffel-run path/to/program.stfbin main
```

## Standard Library

StoffelVM includes essential built-in functions:

- **`print`**: Output values to console
- **`create_object`**: Create new objects
- **`create_array`**: Create new arrays
- **`get_field`/`set_field`**: Object/array field access
- **`array_length`/`array_push`**: Array operations
- **`create_closure`/`call_closure`**: Closure operations
- **`get_upvalue`/`set_upvalue`**: Upvalue management
- **`type`**: Runtime type information

## Hook System

The VM provides a configurable hook system for:

- **Instruction Execution**: Intercept and monitor individual instructions
- **Register Access**: Track register reads and writes
- **Activation Stack**: Monitor function calls and returns
- **Memory Operations**: Debug object and array operations
- **MPC Integration**: Protocol-specific hooks for secret operations

## Performance Characteristics

### Register-Based Advantages

- **Fewer Instructions**: Direct register operations reduce instruction count
- **Better Optimization**: Easier to optimize compared to stack machines
- **Hardware Mapping**: Natural mapping to CPU registers

### MPC Optimizations

- **Separate Register Spaces**: Efficient handling of clear vs. secret data
- **Batched Operations**: Group operations for better protocol efficiency
- **Memory Layout**: Optimized for secret sharing and reconstruction

## Integration with Ecosystem

### StoffelLang Compilation

The VM executes bytecode generated by the StoffelLang compiler:

```
StoffelLang (.stfl) → Compiler → Bytecode (.stfb) → StoffelVM
```

### Python SDK Integration

The Python SDK provides high-level bindings to the VM:

```python
from stoffel import StoffelProgram

program = StoffelProgram("secure_add.stfl")
program.compile()
result = program.execute_locally({"a": 25, "b": 17})
```

### MPC Protocol Integration

The VM integrates with MPC protocols for secure computation:

```
StoffelVM ↔ MPC Protocols ↔ Network Communication
```

## Future Development

Planned enhancements for StoffelVM:

- **Full MPC Integration**: Complete protocol integration for secure computation
- **Garbage Collection**: Automatic memory management for objects and arrays
- **Exception Handling**: Structured error handling and recovery
- **Tail Call Optimization**: Efficient recursive function calls
- **Just-In-Time Compilation**: Runtime optimization for hot code paths
- **Debugging Tools**: Enhanced debugging and profiling capabilities

## Next Steps

To learn more about StoffelVM:

- **[Instructions and Types](./instructions.md)**: Detailed instruction set reference
- **[Using the VM](./usage.md)**: Practical examples and integration patterns
- **[Built-in Functions](./builtins.md)**: Standard library reference
# Getting Started with Stoffel VM

## Introduction
Stoffel VM is a register-based virtual machine designed for both simplicity and power. It's built in Rust and optimized for performance and safety, with special consideration for multiparty computation (MPC) capabilities.

## Quick Start

### Installation
Currently, Stoffel VM can be used as a library in your Rust projects. Add it to your `Cargo.toml`:

```toml
[dependencies]
stoffel-vm = { git = "https://github.com/Stoffel-Labs/StoffelVM" }
```

### Your First Program
Here's a simple "Hello, World!" program using Stoffel VM:

```rust
use stoffel_vm::core_vm::VirtualMachine;
use stoffel_vm::functions::VMFunction;
use stoffel_vm::instructions::Instruction;
use stoffel_vm::core_types::Value;
use std::collections::HashMap;

fn main() -> Result<(), String> {
    // Create a new VM instance
    let vm = VirtualMachine::new();
    
    // Define a hello world function
    let hello_world = VMFunction {
        name: "hello_world".to_string(),
        parameters: vec![],
        upvalues: vec![],
        parent: None,
        register_count: 1,
        instructions: vec![
            // Load string into register 0
            Instruction::LDI(0, Value::String("Hello, World!".to_string())),
            // Push as argument for print
            Instruction::PUSHARG(0),
            // Call print function
            Instruction::CALL("print".to_string()),
            // Return void
            Instruction::RET(0),
        ],
        labels: HashMap::new(),
    };
    
    // Register and execute
    vm.register_function(hello_world);
    vm.execute("hello_world")?;
    
    Ok(())
}
```

## Core Concepts

### 1. Register-Based Architecture
Stoffel VM uses registers instead of a stack for primary computation. Each function has its own set of registers:
- Registers are numbered starting from 0
- Register count is specified per function
- Values can be moved between registers using `MOV`

### 2. Value Types
The VM supports several value types:
- `Int`: 64-bit integers
- `Float`: Fixed-point numbers
- `Bool`: Boolean values
- `String`: UTF-8 strings
- `Object`: Key-value stores
- `Array`: Indexed collections
- `Closure`: Function closures
- `Foreign`: External Rust objects
- `Unit`: Void/null value

### 3. Instructions
Basic instruction categories:

#### Memory Operations
```rust
LDI(reg, value)    // Load immediate value
MOV(dest, src)     // Move between registers
PUSHARG(reg)       // Push argument for function call
```

#### Arithmetic
```rust
ADD(dest, src1, src2)
SUB(dest, src1, src2)
MUL(dest, src1, src2)
DIV(dest, src1, src2)
```

#### Control Flow
```rust
JMP(label)         // Unconditional jump
JMPEQ(label)       // Jump if equal
CALL(function)     // Call function
RET(reg)           // Return value
```

### 4. Functions
Functions in Stoffel VM have:
- A unique name
- Parameter list
- Register count
- Instruction sequence
- Optional upvalues for closures

Example function definition:
```rust
let function = VMFunction {
    name: "add".to_string(),
    parameters: vec!["a".to_string(), "b".to_string()],
    upvalues: vec![],
    parent: None,
    register_count: 3,
    instructions: vec![
        Instruction::ADD(2, 0, 1),
        Instruction::RET(2),
    ],
    labels: HashMap::new(),
};
```

### 5. Built-in Functions
Stoffel VM provides several built-in functions:
- `print`: Output values
- `create_object`: Create new objects
- `create_array`: Create arrays
- `get_field`/`set_field`: Object/array manipulation
- `type`: Get value type

## Debugging
Stoffel VM includes a powerful hook system for debugging:

```rust
vm.register_hook(
    |event| matches!(event, HookEvent::BeforeInstructionExecute(_)),
    move |event, ctx| {
        println!("Executing: {:?}", event);
        Ok(())
    },
    100
);
```

## Best Practices

1. **Register Management**
    - Keep register count minimal
    - Reuse registers when possible
    - Document register usage

2. **Error Handling**
    - Always check function return values
    - Use the hook system for debugging
    - Handle division by zero

3. **Memory Efficiency**
    - Release foreign objects when done
    - Clear arrays/objects when no longer needed
    - Be mindful of closure captures

4. **Performance Tips**
    - Use immediate values when possible
    - Minimize function calls in loops
    - Prefer register operations over memory

## Advanced Features

### Closures
Closures capture their environment:
```rust
// Create a counter
let create_counter = VMFunction {
    name: "create_counter".to_string(),
    parameters: vec!["start".to_string()],
    upvalues: vec![],
    instructions: vec![
        // Create closure with upvalue
        Instruction::LDI(1, Value::String("increment".to_string())),
        Instruction::PUSHARG(1),
        Instruction::LDI(2, Value::String("start".to_string())),
        Instruction::PUSHARG(2),
        Instruction::CALL("create_closure".to_string()),
        Instruction::RET(0),
    ],
    // ...
};
```

### Foreign Functions
Integrate Rust functions:
```rust
vm.register_foreign_function("double", |ctx| {
    match &ctx.args[0] {
        Value::Int(n) => Ok(Value::Int(n * 2)),
        _ => Err("Expected integer".to_string()),
    }
});
```

## Common Patterns

### 1. Looping
```rust
// Basic loop structure
let mut labels = HashMap::new();
labels.insert("loop_start".to_string(), 1);
labels.insert("loop_end".to_string(), 6);

vec![
    // Initialize counter
    Instruction::LDI(0, Value::Int(0)),
    // Compare
    Instruction::CMP(0, 1),
    Instruction::JMPEQ("loop_end".to_string()),
    // Loop body
    // ...
    Instruction::JMP("loop_start".to_string()),
]
```

### 2. Conditional Execution
```rust
vec![
    Instruction::CMP(0, 1),
    Instruction::JMPNEQ("else_branch".to_string()),
    // if branch
    // ...
    Instruction::JMP("end_if".to_string()),
    // else branch
    // ...
]
```

## Further Reading
- Check the [examples](https://github.com/Stoffel-Labs/StoffelVM/tree/main/examples) directory for more complex programs
- Review the [test cases](https://github.com/Stoffel-Labs/StoffelVM/blob/0e8543c2c9953dfd9d309af56258e2df1130c106/src/core_vm.rs#L542) for implementation details
- Explore the [hook system](https://github.com/Stoffel-Labs/StoffelVM/blob/0e8543c2c9953dfd9d309af56258e2df1130c106/src/core_vm.rs#L2187) for debugging

## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
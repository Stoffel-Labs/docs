# VM Functions in Stoffel

This page explains how VM functions are defined and structured in Stoffel's virtual machine.

## Rationale

VM functions form the core executable units in Stoffel. They provide a structured way to define reusable code that can be called from different parts of a program. Each function maintains its own isolated environment with local variables and registers, while still allowing controlled access to outer scopes through upvalues. This design enables modular programming within the constraints of a register-based VM architecture, supporting both MPC operations and conventional programming patterns.

## Comprehensive Overview

A VM function in Stoffel consists of a series of instructions that operate on registers, along with metadata describing the function's interface and requirements. Functions are identified by name and can accept parameters, capture variables from outer scopes, and maintain their own set of registers.

The VM functions use a register-based execution model where values are primarily stored and manipulated in numbered registers. This approach offers efficient instruction encoding and execution compared to stack-based alternatives, which is particularly important for the performance-sensitive operations in MPC applications.

## VM Function Structure

- `name: String`:
  The unique identifier for the function.
  - Used for function lookup during calls
  - Appears in debug output and error messages
  - Must be unique within the VM's function registry

- `parameters: Vec<String>`:
  Names of the function's input parameters.
  - Defines the expected arguments when calling the function
  - Parameter values are loaded into consecutive registers starting from r0
  - Also available by name through the locals map in the activation record

- `upvalues: Vec<String>`:
  Variables to be captured from outer scopes.
  - Enables lexical scoping and closure functionality
  - Listed separately from parameters to clearly identify captured variables
  - Accessed through special upvalue operations rather than direct register access

- `parent: Option<String>`:
  The name of the parent function, if this is a nested function.
  - Supports lexical scoping for nested function definitions
  - Helps with upvalue resolution during closure creation
  - Set to None for top-level functions

- `register_count: usize`:
  The number of registers required by this function.
  - Pre-allocated when the function is called
  - Determines the size of the register array in the activation record
  - Should be large enough for parameters, local computations, and function calls

- `instructions: Vec<Instruction>`:
  The sequence of instructions that comprise the function body.
  - Executed sequentially unless modified by control flow instructions
  - Each instruction typically operates on registers
  - Can include function calls, arithmetic operations, comparisons, etc.

- `labels: HashMap<String, usize>`:
  Maps label names to instruction indices for jump targets.
  - Used to resolve symbolic labels in jump instructions
  - Enables structured control flow (if/else, loops, etc.)
  - Not included in hash calculations for performance reasons

## Execution Model

When a VM function is called:

1. A new activation record is created with registers initialized to the Unit value
2. Function parameters are copied into the first N registers and also into the locals map
3. Upvalues are set up according to the function's declaration
4. The instruction pointer is set to 0
5. Execution begins at the first instruction and continues until a RET instruction is encountered
6. The value in the specified register is returned to the caller

VM functions use a register-based model where most operations involve reading from and writing to numbered registers. This approach provides efficient instruction encoding and execution compared to stack-based alternatives.

## Control Flow

Control flow within VM functions is managed through:

- Labels: Named positions in the instruction sequence
- Jump instructions: Unconditional (JMP) and conditional (JMPEQ, JMPNEQ) transfers of control
- Function calls: Temporary transfer of control to another function
- Return instruction: Exit from the current function back to the caller

Labels are defined in the `labels` map, which associates string names with instruction indices. Jump instructions reference these labels by name, and the VM resolves them to the appropriate instruction index during execution.

## Usage Example

Here's an example of a factorial function implementation:

```rust
let mut labels = HashMap::new();
labels.insert("base_case".to_string(), 6);
labels.insert("recursive_case".to_string(), 8);

let factorial_function = VMFunction {
    name: "factorial".to_string(),
    parameters: vec!["n".to_string()],
    upvalues: Vec::new(),
    parent: None,
    register_count: 5,
    instructions: vec![
        // Check if n <= 1
        Instruction::LDI(1, Value::Int(1)),               // r1 = 1
        Instruction::CMP(0, 1),                           // Compare n with 1
        Instruction::JMPEQ("base_case".to_string()),      // If n == 1, go to base case
        Instruction::CMP(1, 0),                           // Compare 1 with n
        Instruction::JMPNEQ("recursive_case".to_string()), // If not equal, go to recursive case
        Instruction::JMP("base_case".to_string()),
        // base_case: (n <= 1)
        Instruction::LDI(0, Value::Int(1)),               // Return 1
        Instruction::RET(0),
        // recursive_case: (n > 1)
        Instruction::MOV(3, 0),                           // r3 = n
        Instruction::LDI(1, Value::Int(1)),               // r1 = 1
        Instruction::SUB(2, 0, 1),                        // r2 = n - 1
        Instruction::PUSHARG(2),
        Instruction::CALL("factorial".to_string()),
        Instruction::MUL(0, 3, 0),                        // r0 = n * factorial(n-1)
        Instruction::RET(0),
    ],
    labels,
};
```

This example demonstrates a recursive implementation of the factorial function, showcasing the use of registers, labels, conditional jumps, and recursive function calls.
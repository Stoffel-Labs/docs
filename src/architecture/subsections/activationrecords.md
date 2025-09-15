# Activation Records in Stoffel

This page explains the concept of activation records in Stoffel's virtual machine, their structure, and how they're used during program execution.

## Rationale

Activation records are a fundamental component of Stoffel's execution model, designed to maintain the state of function calls in a structured manner. They provide isolation between different function calls while supporting the runtime's ability to handle both VM functions and foreign functions within the same execution context. The activation record approach creates clear boundaries between different execution contexts and helps organize program state.

## Comprehensive Overview

An activation record represents a single function invocation in the Stoffel VM. Each time a function is called, a new activation record is created and pushed onto the VM's stack of records. When the function returns, its activation record is popped from the stack.

The VM maintains a stack of activation records, with the topmost record representing the currently executing function. This stack grows and shrinks as functions are called and return, implementing the expected call-and-return semantics of structured programming.

Activation records are particularly important for the `CALL` instruction and for managing the execution of both VM functions and foreign functions. They store all the state necessary to execute a function, including local variables, registers, function arguments, and execution state.

## Structure of Activation Records

- `function_name: String`:
  Stores the name of the function this record represents.
    - Used for debugging and error reporting
    - Allows for lookup of function definitions when needed

- `locals: HashMap<String, Value>`:
  Maps variable names to their values within the function scope.
    - Allows named access to local variables
    - Persists values throughout the function's lifetime

- `registers: Vec<Value>`:
  Array of register values used during function execution.
    - Register 0 is typically used for return values
    - Function parameters are loaded into consecutive registers starting from 0
    - Size is determined by the function's register count declaration

- `upvalues: Vec<Upvalue>`:
  Captured values from outer scopes, used for closures.
    - Enables lexical scoping and closure functionality
    - Allows inner functions to access variables from their enclosing scopes

- `instruction_pointer: usize`:
  Current position in the function's instruction sequence.
    - Tracks which instruction is currently being executed
    - Updated after each instruction execution

- `stack: Vec<Value>`:
  Temporary storage for function arguments and local operations.
    - Used to pass arguments to functions via the `PUSHARG` instruction
    - Cleared after arguments are processed during function calls

- `compare_flag: i32`:
  Stores the result of the most recent comparison operation.
    - Value of 0 indicates equality
    - Negative values indicate less-than relationship
    - Positive values indicate greater-than relationship

## Lifecycle of Activation Records

Activation records are created and managed at several key points during program execution:

1. **Program Initialization**:
   When the VM starts executing a program, it creates an initial activation record for the main function (or specified entry point).

2. **Function Calls**:
   The `CALL` instruction creates a new activation record, sets up function parameters from the caller's stack, and pushes it onto the activation record stack.

3. **Closure Execution**:
   When executing closures, the VM creates an activation record that includes the upvalues captured from the closure's defining environment.

4. **Function Return**:
   The `RET` instruction pops the current activation record off the stack, returning control to the caller function with the specified return value.

## Usage in Function Execution

When a function is called using the `CALL` instruction:

1. Arguments are collected from the caller's stack
2. A new activation record is created with:
    - Function name set to the called function
    - Register space allocated according to the function's requirements
    - Instruction pointer initialized to 0
    - Compare flag set to 0
3. Arguments are copied into the new record's registers and locals
4. The caller's stack is cleared of the passed arguments
5. VM execution continues with the new activation record

For foreign functions, the VM:
1. Prepares the function arguments
2. Invokes the foreign function with a context containing those arguments
3. Handles the result without creating a traditional activation record
4. Maintains stack integrity throughout the call
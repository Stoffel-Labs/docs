# Stoffel Virtual Machine Architecture

This page explains the overall architecture of Stoffel's virtual machine, its core components, and how they work together to execute programs.

## Rationale

The Stoffel VM uses a register-based architecture designed to efficiently execute programs while maintaining clear execution boundaries. This approach provides a balance between performance and flexibility, enabling the VM to handle both simple scripts and complex applications with multiple function calls, closures, and data structures. The design emphasizes a clean separation between different execution contexts through the activation record system, allowing for intuitive debugging and predictable behavior.

## Comprehensive Overview

Stoffel is implemented as a register-based virtual machine that executes bytecode instructions. The VM is designed around several key components that work together to provide a complete execution environment:

1. **VMState**: The core state of the virtual machine
2. **VirtualMachine**: The primary interface for interacting with the VM
3. **Activation Records**: Function execution contexts
4. **Value System**: The type system for data manipulation
5. **Instruction Set**: The operations that the VM can perform
6. **Hook System**: The instrumentation and debugging framework

These components provide a complete execution environment for running programs written in Stoffel bytecode. The VM's design emphasizes simplicity, predictability, and maintainability, making it suitable for a wide range of applications.

## VM State

The central component of the VM architecture is the `VMState` struct, which maintains the current execution state:

- `functions`: A registry of all available functions (both VM and foreign)
- `activation_records`: The call stack of active function invocations
- `current_instruction`: The currently executing instruction
- `object_store`: Central storage for objects and arrays
- `foreign_objects`: Storage for external/native objects
- `hook_manager`: System for registering and triggering event hooks

The `VMState` provides methods for executing instructions, managing the activation record stack, and interacting with the hook system. It serves as the core runtime state that the VM manipulates during program execution.

## Virtual Machine Interface

The `VirtualMachine` struct provides the primary interface for interacting with the VM:

- Manages the VM state using a `Mutex` for thread safety
- Offers methods for registering and executing functions
- Provides a standard library of built-in functions
- Exposes the hook system for instrumentation and debugging

This interface abstracts the complexity of the underlying VM implementation, offering a clean API for running programs, extending the VM with new functions, and monitoring execution.

## Execution Model

Stoffel uses a register-based execution model with the following characteristics:

1. **Program Loading**: Functions are registered with the VM, either as VM functions (bytecode) or foreign functions (native code)
2. **Execution Initialization**: An initial activation record is created for the main function
3. **Instruction Execution**: The VM executes instructions sequentially, updating registers and the VM state
4. **Function Calls**: When a function is called, a new activation record is pushed onto the stack
5. **Function Returns**: When a function returns, its activation record is popped from the stack
6. **Completion**: Execution completes when the main function returns or an error occurs

This model provides a straightforward execution flow while supporting complex behaviors like recursion, closures, and foreign function integration.

## Function Dispatch

The VM supports two types of functions:

- **VM Functions**: Defined as bytecode instructions that the VM executes directly
- **Foreign Functions**: Implemented in Rust and registered with the VM

When a function is called, the VM determines its type and handles it accordingly:

1. **VM Function Execution**:
   - Create a new activation record
   - Set up function parameters as registers and locals
   - Execute instructions until a return occurs

2. **Foreign Function Execution**:
   - Prepare function arguments
   - Create a function context with arguments and VM state
   - Execute the Rust function
   - Process the return value and update register 0

This dual approach allows for a flexible mix of interpreted and native code, enabling performance optimizations and system integrations where needed.

## Concurrency and Thread Safety

The VM is designed with thread safety in mind:

- The `VMState` is wrapped in a `Mutex` to prevent concurrent access
- Foreign objects use `Arc<Mutex<T>>` for thread-safe reference counting
- Closures use `Arc<Closure>` to allow safe sharing

This design allows the VM to be used in multi-threaded applications, with appropriate synchronization to prevent data races and ensure consistent state.

## Error Handling

The VM uses a Result-based error handling approach:

- Functions return `Result<Value, String>` to indicate success or failure
- Errors include descriptive messages about the issue encountered
- The VM propagates errors up the call stack to the original caller
- Hook callbacks can also return errors that will abort execution

This approach provides clear error information while allowing the VM to fail gracefully and provide useful feedback for debugging.

## Instruction Execution Loop

The core of the VM is the instruction execution loop in `execute_until_return()`:

1. Retrieve the current function and instruction pointer
2. Load the next instruction
3. Trigger the `BeforeInstructionExecute` hook
4. Execute the instruction, updating VM state as needed
5. Trigger the `AfterInstructionExecute` hook
6. Continue until a return or error occurs

This loop handles all VM instructions, managing the execution flow and state updates according to the instruction semantics.

## Memory Management

Stoffel uses Rust's memory management system for automatic reference counting and garbage collection:

- Values are cloned when passed between contexts, avoiding aliasing issues
- Complex values (objects, arrays, closures) use reference counting via `Arc`
- Foreign objects use `Arc<Mutex<T>>` for safe shared access
- The VM does not require explicit memory management by users

This approach provides memory safety without requiring manual memory management or a complex garbage collector implementation.

## Component Integration

The VM's components are tightly integrated to provide a cohesive execution environment:

- The instruction set operates on the activation record's registers and stack
- Functions interact with the object store for object and array operations
- Hooks provide visibility into VM operations across all components
- Foreign functions access the VM state through a controlled context interface

This integration ensures that the VM components work together smoothly while maintaining proper encapsulation and separation of concerns.

## Performance Considerations

The VM design incorporates several performance optimizations:

- Register-based operation reduces stack manipulation overhead
- Direct function dispatch avoids interpreter overhead for foreign functions
- Object operations use indexed lookups for efficient access
- Hook system can be selectively enabled or disabled for performance-critical code
- Instruction execution is optimized for common operations

While not a JIT compiler, the VM provides reasonable performance for many applications, with the ability to use foreign functions for performance-critical code.
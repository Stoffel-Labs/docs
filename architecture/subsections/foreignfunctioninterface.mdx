# Foreign Functions in Stoffel

This page explains how foreign functions are implemented in Stoffel's virtual machine, their structure, and how they interact with the VM's execution environment.

## Rationale

Foreign functions extend Stoffel's capabilities by allowing integration with the host environment. They enable the VM to access functionality that would be difficult or inefficient to implement within the VM's instruction set, such as file I/O, object creation, and specialized algorithms. The foreign function mechanism provides a bridge between the VM and the host environment while maintaining a clean separation between the two.

## Comprehensive Overview

Foreign functions in Stoffel are implemented as Rust closures that operate on VM values and can modify VM state. Each foreign function is registered with the VM under a string name and can then be called from within Stoffel programs using the same calling convention as regular VM functions.

The foreign function mechanism uses a context-based approach where each function receives a context object containing its arguments and a mutable reference to the VM state. This design gives foreign functions full access to the VM's internal state while maintaining a clean API boundary.

## Foreign Function Structure

- `ForeignFunctionPtr`:
  The core type representing a foreign function implementation.
  - Wrapped in an `Arc` (atomic reference counter) for thread-safe sharing
  - Takes a `ForeignFunctionContext` parameter providing access to arguments and VM state
  - Returns a `Result<Value, String>` indicating success or failure with an error message

- `ForeignFunction`:
  A wrapper structure for registered foreign functions.
  - `name`: String identifier used to reference the function
  - `func`: The actual function implementation as a `ForeignFunctionPtr`

- `ForeignFunctionContext`:
  The execution context passed to foreign function implementations.
  - `args`: A slice containing the function's arguments as `Value` objects
  - `vm_state`: A mutable reference to the current `VMState`, allowing full access to VM internals

## Registering Foreign Functions

Foreign functions are registered with the VM using a registration API that takes a name and a function implementation:

1. The VM creates a `ForeignFunction` struct with the provided name and function implementation
2. The function is wrapped in an `Arc` for thread-safe sharing
3. The `ForeignFunction` is stored in the VM's `functions` map under its name
4. The function can then be called from Stoffel code using its registered name

## Calling Foreign Functions

When a foreign function is called, either directly or through the `CALL` instruction:

1. The VM locates the function in its registry by name
2. It creates a `ForeignFunctionContext` with:
   - A reference to the arguments array
   - A mutable reference to the current VM state
3. The VM triggers a `BeforeFunctionCall` hook event
4. The function is executed with the context
5. The result is captured and the VM triggers an `AfterFunctionCall` hook event
6. The result is returned to the caller or stored in register 0

Unlike VM functions, foreign functions don't create a new activation record. Instead, they execute within the context of the calling function and can modify the VM state directly.

## VM State Access

Foreign functions have full access to the VM's internal state through the `vm_state` field of the context:

- `functions`: Registry of all VM and foreign functions
- `activation_records`: The stack of function calls currently being executed
- `current_instruction`: The current instruction pointer
- `object_store`: Storage for Stoffel objects and arrays
- `foreign_objects`: Storage for host environment objects
- `hook_manager`: Event hook system for debugging and monitoring

This access allows foreign functions to implement complex behaviors that would be difficult to express in the VM's instruction set, such as object creation, array manipulation, and integration with host environment resources.

## Standard Library Implementation

Many of Stoffel's standard library functions are implemented as foreign functions, including:

- Object and array creation and manipulation
- Closure creation and management
- Type information access

These functions provide the essential building blocks for Stoffel programs while abstracting away the complexity of their implementation details.
# Closures in Stoffel

This page explains how closures are implemented and used in Stoffel's virtual machine, their structure, and their role in the programming model.

## Rationale

Closures in Stoffel enable higher-order functions and maintain lexical scoping semantics, providing a flexible programming model. The implementation uses a deep-copy approach for captured values to ensure predictable behavior across different execution contexts. This design choice allows developers to use functional programming patterns while maintaining clear boundaries between execution environments.

## Comprehensive Overview

A closure in Stoffel represents a function combined with its lexical environment (captured upvalues). Closures are first-class values that can be created, passed as arguments, returned from functions, and invoked. The VM implements closures through a combination of the core `Closure` struct, specialized foreign functions for closure management, and integration with the activation records.

The closure implementation follows a deep-copy model, where captured values are duplicated rather than referenced. This approach ensures that each closure maintains its own independent state, avoiding unexpected interactions between different parts of the program.

## Closure Structure

- `function_id: String`:
  The name of the function wrapped by the closure.
    - Used to locate the function definition in the VM's function registry
    - Enables the VM to know which code to execute when the closure is called

- `upvalues: Vec<Upvalue>`:
  The collection of captured variables from the closure's defining environment.
    - Each upvalue contains a name and its associated value
    - Enables access to variables from outer scopes when the closure executes
    - Stored as deep copies to maintain independent state

## Creating Closures

Closures are created using the `create_closure` foreign function, which takes a function name and a list of variable names to capture:

1. The function validates that a function with the specified name exists
2. For each variable name to capture, the VM:
    - Searches the current scope chain for the named value
    - Creates a new upvalue containing a deep copy of the found value
    - Adds the upvalue to the closure's environment

The deep copying of upvalues ensures that each closure has its own independent set of values, which means changes to the original variables don't affect the closure's behavior after creation.

## Calling Closures

Closures are invoked using the `call_closure` foreign function, which takes a closure and its arguments:

1. The function extracts the function ID and upvalues from the closure
2. It validates that the function exists and has the correct arity
3. It creates a new activation record with:
    - The function's name
    - A fresh set of registers
    - Copies of the closure's upvalues
    - The function arguments loaded into registers and locals
4. The new activation record is pushed onto the VM's stack, transferring control to the function

This approach ensures that each closure call has its own isolated environment while maintaining access to the captured variables, preserving the expected lexical scoping semantics.

## Accessing Upvalues

Within a closure, upvalues are accessed using specialized foreign functions:

- `get_upvalue(name)`:
  Retrieves the current value of a captured variable.
    - Searches the current activation record's upvalues for the named value
    - Triggers an `UpvalueRead` event for debugging
    - Returns a copy of the upvalue's current value

- `set_upvalue(name, value)`:
  Updates the value of a captured variable.
    - Searches the current activation record's upvalues for the named value
    - Updates the upvalue with the new value
    - Triggers an `UpvalueWrite` event for debugging
    - Changes are local to the current closure instance

These operations maintain the isolation between different closure instances, as each instance has its own copy of the upvalues rather than sharing references.
# Stoffel Standard Library

This page provides an overview of the built-in functions available in Stoffel's standard library and how they can be used in programs.

## Rationale

The standard library provides essential functionality that bridges the gap between the VM's core instruction set and higher-level operations needed for practical programming. These built-in functions are implemented as foreign functions, allowing them to interact directly with the VM's internal state. The standard library focuses on common operations for working with complex data structures and closures, enabling programmers to build more sophisticated applications.

## Comprehensive Overview

Stoffel's standard library provides functions in several key areas: object and array manipulation, closure handling, and basic utilities. Each function is registered as a foreign function within the VM, enabling direct access to the VM's internal state in a controlled manner. These functions complement the instruction set by providing higher-level operations that would be cumbersome to implement with the basic instructions alone.

The standard library functions follow a consistent error-handling pattern, returning appropriate error messages when called with incorrect arguments. Most functions interact with the VM's hook system, triggering events that allow for monitoring and debugging of program execution.

## Object Manipulation

- `create_object()`:
  Creates a new empty object in the VM's object store.
  - Returns: A new Object value with a unique ID

- `get_field(object, key)`:
  Retrieves a field value from an object or array.
  - `object`: The object or array to query
  - `key`: The field name or array index to retrieve
  - Returns: The value of the field, or Unit if not found
  - Triggers: ObjectFieldRead or ArrayElementRead event

- `set_field(object, key, value)`:
  Sets a field value in an object or array.
  - `object`: The object or array to modify
  - `key`: The field name or array index to set
  - `value`: The value to store in the field
  - Returns: Unit
  - Triggers: ObjectFieldWrite or ArrayElementWrite event

## Array Operations

- `create_array([capacity])`:
  Creates a new empty array, optionally with specified capacity.
  - `capacity` (optional): The initial capacity of the array as an integer
  - Returns: A new Array value with a unique ID

- `array_length(array)`:
  Gets the length of an array.
  - `array`: The array to query
  - Returns: The length of the array as an integer
  - Throws: Error if the argument is not an array

- `array_push(array, value, ...)`:
  Adds one or more values to the end of an array.
  - `array`: The array to modify
  - `value, ...`: One or more values to append to the array
  - Returns: The new length of the array
  - Throws: Error if the first argument is not an array

## Closure Handling

- `create_closure(function_name, [upvalue_names...])`:
  Creates a new closure for the specified function.
  - `function_name`: The name of the function to wrap in a closure
  - `upvalue_names` (optional): Names of variables to capture from the current scope
  - Returns: A new Closure value
  - Triggers: ClosureCreated event
  - Notes: Each captured upvalue is a deep copy of the original value

- `call_closure(closure, [args...])`:
  Calls a closure with the specified arguments.
  - `closure`: The closure to call
  - `args...` (optional): Arguments to pass to the closure function
  - Returns: Unit (result will be in register 0 of the caller)
  - Throws: Error if the function is not found or argument count is incorrect
  - Notes: Creates a new activation record with the closure's upvalues

- `get_upvalue(name)`:
  Retrieves a captured upvalue by name from the current activation record.
  - `name`: The name of the upvalue to retrieve
  - Returns: The current value of the upvalue
  - Throws: Error if the upvalue is not found
  - Triggers: UpvalueRead event

- `set_upvalue(name, value)`:
  Modifies a captured upvalue in the current activation record.
  - `name`: The name of the upvalue to modify
  - `value`: The new value for the upvalue
  - Returns: Unit
  - Throws: Error if the upvalue is not found
  - Triggers: UpvalueWrite event

## Utility Functions

- `print(values...)`:
  Prints one or more values to the standard output.
  - `values...`: Values to print, space-separated
  - Returns: Unit
  - Notes: Automatically stringifies values, with special handling for strings

- `type(value)`:
  Determines the type of a `Value`.
  - `value`: The value to check
  - Returns: A string indicating the type ("integer", "float", "boolean", "string", "object", "array", "userdata", "function", or "nil")
# Value Types in Stoffel

This page explains the value types and data structures available in Stoffel's virtual machine, their properties, and how they're managed during program execution.

## Rationale

Stoffel's type system is designed to provide the fundamental building blocks needed for practical programming. By implementing a carefully selected set of primitive and composite types, Stoffel enables developers to create complex data structures and algorithms while maintaining consistent behavior across different execution contexts.

## Comprehensive Overview

Stoffel's type system includes primitive values (integers, floats, booleans, strings), composite values (objects, arrays), and function values (closures). Each value is represented by the `Value` enum, which encapsulates both the type and data of a value.

The VM maintains separate storage mechanisms for different composite types. Objects and arrays are managed through the `ObjectStore`, which assigns unique identifiers to each instance. This reference-based approach allows for efficient manipulation of complex data structures while maintaining proper isolation between different parts of a program.

## Primitive Types

- `Int(i64)`:
  Represents integer values.
  - Used for counting, indexing, and whole-number arithmetic
  - Supports all standard arithmetic and bitwise operations

- `Float(i64)`:
  Represents floating-point values using fixed-point representation.
  - Stored as fixed-point (scaled integers) for consistent behavior
  - Maintains equality and hashability
  - Display format converts to standard floating-point notation

- `Bool(bool)`:
  Represents boolean values.
  - Used for logical operations and conditional expressions
  - Values are either `true` or `false`

- `String(String)`:
  Represents text data.
  - Used for identifiers, keys, and textual content
  - Immutable once created

- `Unit`:
  Represents the absence of a value.
  - Similar to `null` or `void` in other languages
  - Used as default return value for functions with no explicit return

## Composite Types

- `Object(usize)`:
  Represents a key-value mapping structure.
  - Reference to an object in the VM's object store
  - Fields can be accessed using any value type as keys
  - Supports dynamic addition and modification of fields

- `Array(usize)`:
  Represents an ordered collection of values.
  - Reference to an array in the VM's array store
  - Optimized for integer-indexed access starting from 1
  - Supports both dense and sparse representations
  - Also allows non-integer keys for associative array behavior

## Function Types

- `Closure(Arc<Closure>)`:
  Represents a function with its captured environment.
  - Contains a reference to a function and its upvalues
  - Enables higher-order functions and callbacks
  - Preserves lexical scoping through upvalue capture

## Foreign Values

- `Foreign(usize)`:
  Represents a reference to an external object.
  - Enables integration with host environment resources
  - Type-safety maintained through dynamic type checking
  - Allows extension of the VM with custom types and operations

## Arrays

Arrays in Stoffel are implemented as a hybrid data structure:

- `elements`: A contiguous vector of values for efficient integer-indexed access
- `extra_fields`: A hash map for sparse or non-integer indices
- Integer indices start from 1 (following traditional scripting language conventions)
- Arrays automatically grow when elements are added at the end
- Sparse indices are handled efficiently to avoid wasting memory

## Objects

Objects in Stoffel are implemented as general purpose key-value stores:

- `fields`: A hash map supporting any value type as both keys and values
- No predefined structure, allowing for dynamic addition and removal of fields
- Enables flexible data modeling patterns, including record and dictionary styles

## Object Store

The `ObjectStore` provides centralized management of objects and arrays:

- Assigns unique numeric identifiers to each instance
- Maintains separate collections for objects and arrays
- Provides controlled access through getter methods
- Handles field access and modification with appropriate type checking
- Ensures proper isolation between different data instances

## Foreign Object Storage

The `ForeignObjectStorage` enables safe integration with external types:

- Type-erased storage through the `AnyObject` trait
- Type-safe retrieval using generics and downcasting
- Thread-safe access using `Arc<Mutex<T>>` for concurrent operations
- Allows extension of the VM with custom native types

## Upvalues and Closures

Closures in Stoffel capture their lexical environment through upvalues:

- `Upvalue`: A named variable captured from an outer scope
- `Closure`: A function combined with its captured upvalues
- Upvalues maintain a deep copy of the captured values
- Ensures predictable behavior across different execution contexts
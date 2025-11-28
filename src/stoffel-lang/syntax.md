# Syntax and Examples

This page provides a comprehensive guide to StoffelLang syntax, featuring practical examples and detailed explanations of the language's features.

## Basic Elements

### Comments

StoffelLang uses `#` for comments:

```
# This is a single-line comment
var x = 42  # Inline comment

# Multi-line comments can be created
# by using multiple single-line comments
```

### Identifiers and Keywords

**Valid identifiers:**
- Must start with a letter or underscore
- Can contain letters, numbers, and underscores
- Case-sensitive

```
var my_variable = 10
var _private_value = "secret"
var camelCase = true
var snake_case_name = "Alice"
```

**Reserved keywords:**
```
var def type object enum main
if else elif while for in
return break continue
true false nil secret discard
```

## Variables and Types

### Variable Declarations

StoffelLang uses `var` for variable declarations:

```
# Variable with type inference
var name = "Alice"
var age = 25
var is_active = true

# Variable with explicit type annotation
var counter: int64 = 0
var status: string = "pending"

# Variable declaration without initialization (requires type)
var result: int64
```

### Type Annotations

Explicit type annotations use colon syntax:

```
var count: int64 = 100
var message: string = "Hello"
var flag: bool = false
```

### Type Inference

StoffelLang can infer types from context:

```
var inferred_int = 42        # int64
var inferred_string = "text" # string
var inferred_bool = true     # bool
```

## Primitive Types

### Integer Types

StoffelLang supports multiple integer types:

```
# Signed integers
var a: int64 = 100
var b: int32 = 50
var c: int16 = 25
var d: int8 = 10

# Unsigned integers
var e: uint64 = 100
var f: uint32 = 50
var g: uint16 = 25
var h: uint8 = 10

# Typed integer literals
var typed_i64 = 42i64
var typed_u32 = 100u32
var typed_i8 = 127i8
```

### Boolean Type

```
var is_ready: bool = true
var is_complete: bool = false
```

### String Type

```
var greeting: string = "Hello, world!"
var empty_string: string = ""
```

### Nil Type

```
var nothing = nil
```

## Secret Types

The `secret` keyword creates MPC-aware types for secure computation:

```
# Secret variable declaration
secret var my_secret = 42

# Secret with explicit type
var secret_value: secret int64 = 100

# Secret function parameter
def process_secret(data: secret int64) -> secret int64:
    return data * 2
```

**Important Constraints:**
- Secret values **cannot** be used in `if` or `while` conditions
- Comparisons involving secrets produce secret boolean results
- Use `ClientStore.take_share()` to get secret inputs from MPC clients

## Functions

### Function Definitions

Functions use the `def` keyword:

```
# Basic function
def greet(name: string) -> string:
    return "Hello, " + name

# Function with multiple parameters
def add(a: int64, b: int64) -> int64:
    return a + b

# Function without return value
def log_message(msg: string) -> nil:
    print(msg)

# Function with secret parameters
def secure_multiply(a: secret int64, b: secret int64) -> secret int64:
    return a * b
```

### Entry Point

The program entry point uses the `main` keyword:

```
main main() -> int64:
    return 42
```

### Function Calls

```
# Basic function calls
var result = add(10, 20)
var greeting = greet("Alice")

# Nested function calls
var complex_result = add(add(1, 2), add(3, 4))
```

### Functions with Local Variables

```
def calculate_area(length: int64, width: int64) -> int64:
    var area = length * width
    print("Area calculated")
    return area
```

## Control Flow

### If Statements

```
# Basic if statement
if age >= 18:
    print("Adult")

# If-else
if temperature > 30:
    print("Hot")
else:
    print("Not hot")

# If-elif-else
if score >= 90:
    print("A grade")
elif score >= 80:
    print("B grade")
elif score >= 70:
    print("C grade")
else:
    print("Below C grade")
```

### While Loops

```
# Basic while loop
var count = 0
while count < 10:
    print("Counting")
    count = count + 1
```

### For Loops

```
# Range-based for loops (inclusive)
for i in 0..10:
    print("Number")
```

### Loop Control

```
# Break and continue
var i = 0
while i < 100:
    i = i + 1
    if i == 5:
        continue
    if i == 10:
        break
```

## Operators

### Arithmetic Operators

```
var a = 10
var b = 3

var sum = a + b         # 13
var difference = a - b  # 7
var product = a * b     # 30
var quotient = a / b    # 3 (integer division)
var remainder = a % b   # 1
```

### Comparison Operators

```
var x = 10
var y = 20

var equal = x == y        # false
var not_equal = x != y    # true
var less_than = x < y     # true
var less_equal = x <= y   # true
var greater_than = x > y  # false
var greater_equal = x >= y # false
```

### Bitwise Operators

```
var a = 5   # 0101 in binary
var b = 3   # 0011 in binary

var and_result = a & b    # 1 (0001)
var or_result = a | b     # 7 (0111)
var xor_result = a ^ b    # 6 (0110)
var not_result = ~a       # bitwise NOT
var shift_left = a << 1   # 10
var shift_right = a >> 1  # 2
```

## Built-in Functions

### print

Output text to the console:

```
def greet() -> nil:
    print("Hello, World!")
```

### ClientStore

Access secret inputs from MPC clients:

```
# Get the number of connected clients
var num_clients = ClientStore.get_number_clients()

# Take a secret share from a client
# Must be assigned to a secret variable!
secret var client_input = ClientStore.take_share(0, 0)

# Parameters: (party_id, share_index)
secret var share1 = ClientStore.take_share(0, 0)  # Party 0, share 0
secret var share2 = ClientStore.take_share(1, 0)  # Party 1, share 0
```

**Important:** Results from `ClientStore.take_share()` must be assigned to `secret` variables.

## Working with Secret Types

### Secret Arithmetic

```
def secure_calculation(a: secret int64, b: secret int64) -> secret int64:
    var result = a + b
    return result * 2

def mixed_operation(secret_val: secret int64, public_val: int64) -> secret int64:
    # Public values can be used with secrets
    return secret_val * public_val
```

### MPC Input Pattern

Common pattern for processing client inputs:

```
def process_client_inputs() -> secret int64:
    # Get inputs from two clients
    secret var input1 = ClientStore.take_share(0, 0)
    secret var input2 = ClientStore.take_share(1, 0)

    # Perform secure computation
    return input1 + input2

main main() -> nil:
    var num_clients = ClientStore.get_number_clients()
    secret var result = process_client_inputs()
    print("Computation complete")
```

## Complete Examples

### Fibonacci (Iterative)

```
def fibonacci(n: int64) -> int64:
    if n <= 1:
        return n
    var a: int64 = 0
    var b: int64 = 1
    for i in 2..n:
        var temp = a + b
        a = b
        b = temp
    return b

main main() -> int64:
    return fibonacci(10)
```

### Factorial (Recursive)

```
def factorial(n: int64) -> int64:
    if n <= 1:
        return 1
    return n * factorial(n - 1)

main main() -> int64:
    return factorial(5)  # Returns 120
```

### Secure Sum

```
def secure_sum() -> secret int64:
    var num_clients = ClientStore.get_number_clients()
    secret var total: secret int64 = ClientStore.take_share(0, 0)

    # Note: In practice, you'd loop based on num_clients
    secret var input2 = ClientStore.take_share(1, 0)
    total = total + input2

    return total

main main() -> nil:
    secret var result = secure_sum()
    print("Sum computed")
```

## Data Structures (Planned)

### Object Types

> **Note:** Object types are parsed but have limited code generation support.

```
# Object type definition (planned)
type Person = object
    name: string
    age: int64
```

### Enum Types

> **Note:** Enum types are parsed but have limited code generation support.

```
# Enum definition (planned)
type Status = enum
    Active
    Inactive
    Pending
```

## Best Practices

### Naming Conventions

```
# Use snake_case for variables and functions
var user_name = "alice"
var max_retry_count = 5

def calculate_total_cost(base_price: int64, tax_rate: int64) -> int64:
    return base_price + (base_price * tax_rate / 100)

# Use PascalCase for types (when supported)
type UserAccount = object
    user_id: int64
```

### Secret Type Usage

```
# Clearly distinguish between public and secret data
def process_transaction(
    public_user_id: int64,
    secret_amount: secret int64
) -> secret int64:
    # Perform secure computation
    return secret_amount * 2

# Avoid using secrets in conditions (not allowed!)
# BAD: if secret_value > 0:  # This will fail!
# GOOD: Keep secret values in computations only
```

This syntax guide covers the current StoffelLang implementation. Features marked as "planned" are parsed by the compiler but may have limited code generation support.

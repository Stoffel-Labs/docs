# Syntax and Examples

This page provides a comprehensive guide to StoffelLang syntax, featuring practical examples and detailed explanations of the language's features.

## Basic Elements

### Comments

StoffelLang uses `#` for comments:

```
# This is a single-line comment
let x = 42  # Inline comment

# Multi-line comments can be created
# by using multiple single-line comments
```

### Identifiers and Keywords

**Valid identifiers:**
- Must start with a letter or underscore
- Can contain letters, numbers, and underscores
- Case-sensitive

```
let my_variable = 10
let _private_value = "secret"
let camelCase = true
let snake_case_name = "Alice"
```

**Reserved keywords:**
```
let var proc type object enum
if else elif while for in
return yield break continue
true false nil secret discard
```

## Variables and Types

### Variable Declarations

StoffelLang supports immutable (`let`) and mutable (`var`) variables:

```
# Immutable variables
let name: string = "Alice"
let age: int64 = 25
let is_active = true  # Type inference

# Mutable variables
var counter: int64 = 0
var status = "pending"  # Type inference
```

### Type Annotations

Explicit type annotations use colon syntax:

```
let count: int64 = 100
let message: string = "Hello"
let flag: bool = false
let empty: nil = nil
```

### Type Inference

StoffelLang can infer types from context:

```
let inferred_int = 42        # int64
let inferred_string = "text" # string
let inferred_bool = true     # bool
```

## Primitive Types

### Integer Types

StoffelLang primarily uses `int64`:

```
let small_number: int64 = 10
let large_number: int64 = 9223372036854775807
let negative: int64 = -42
```

### Boolean Type

```
let is_ready: bool = true
let is_complete: bool = false

# Boolean operations
let result = true and false  # false
let combined = true or false # true
let negated = not true       # false
```

### String Type

```
let greeting: string = "Hello, world!"
let empty_string: string = ""
let multiline = "First line\nSecond line"

# String concatenation
let full_name = "Alice" + " " + "Smith"
let message = "Count: " + $42  # Convert int to string with $
```

### Nil Type

```
let nothing: nil = nil
let maybe_value = nil  # Type inferred as nil
```

## Secret Types

The `secret` keyword creates MPC-aware types:

```
# Secret primitive types
let secret_age: secret int64 = 25
let secret_name: secret string = "Bob"
let secret_flag: secret bool = true

# Secret values in computations
proc secure_comparison(a: secret int64, b: secret int64): secret bool =
  return a > b

# Mixed public/secret operations
proc threshold_check(secret_value: secret int64, public_threshold: int64): secret bool =
  return secret_value >= public_threshold
```

## Functions

### Function Definitions

Functions use the `proc` keyword:

```
# Basic function
proc greet(name: string): string =
  return "Hello, " + name

# Function with multiple parameters
proc add(a: int64, b: int64): int64 =
  return a + b

# Function without return value (implicit nil return)
proc log_message(msg: string) =
  print(msg)

# Function with secret parameters
proc secure_multiply(a: secret int64, b: secret int64): secret int64 =
  return a * b
```

### Function Calls

```
# Basic function calls
let result = add(10, 20)
let greeting = greet("Alice")

# Nested function calls
let complex_result = add(add(1, 2), add(3, 4))

# Secret function calls
let secret_result = secure_multiply(secret(5), secret(6))
```

### Functions with Local Variables

```
proc calculate_area(length: int64, width: int64): int64 =
  let area = length * width
  let formatted_msg = "Area calculated: " + $area
  print(formatted_msg)
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

### If Expressions

If statements can be used as expressions:

```
let status = if age >= 18: "adult" else: "minor"
let max_value = if a > b: a else: b
```

### While Loops

```
# Basic while loop
var count = 0
while count < 10:
  print("Count: " + $count)
  count = count + 1

# While with complex condition
var running = true
var attempts = 0
while running and attempts < 5:
  # Do something
  attempts = attempts + 1
  if attempts >= 3:
    running = false
```

### For Loops

```
# Range-based for loops
for i in 0..10:
  print("Number: " + $i)

# For loop with step (conceptual - syntax may vary)
for i in 0..20:
  if i % 2 == 0:
    print("Even: " + $i)
```

## Data Structures

### Object Types

```
# Object type definition
type Person = object
  name: string
  age: int64
  email: string
  is_active: bool

# Object with secret fields
type SecurePerson = object
  name: string
  age: secret int64
  salary: secret int64
  public_id: int64
```

### Object Creation and Access

```
# Creating objects
let alice = Person(
  name: "Alice Smith",
  age: 30,
  email: "alice@example.com",
  is_active: true
)

# Accessing fields
let person_name = alice.name
let person_age = alice.age

# Creating objects with secret fields
let secure_employee = SecurePerson(
  name: "Bob Jones",
  age: secret(35),
  salary: secret(75000),
  public_id: 12345
)
```

### Nested Objects

```
type Address = object
  street: string
  city: string
  country: string

type Employee = object
  personal: Person
  address: Address
  employee_id: int64

let employee = Employee(
  personal: Person(
    name: "Carol Davis",
    age: 28,
    email: "carol@company.com",
    is_active: true
  ),
  address: Address(
    street: "123 Main St",
    city: "Tech City",
    country: "USA"
  ),
  employee_id: 98765
)

# Accessing nested fields
let employee_name = employee.personal.name
let employee_city = employee.address.city
```

### Enum Types (Planned)

```
# Basic enum
type Status = enum
  Active
  Inactive
  Pending
  Suspended

# Enum with values
type Priority = enum
  Low = 1
  Medium = 2
  High = 3
  Critical = 4

# Using enums
let current_status = Status.Active
let task_priority = Priority.High
```

## Operators

### Arithmetic Operators

```
let a = 10
let b = 3

let sum = a + b      # 13
let difference = a - b  # 7
let product = a * b     # 30
let quotient = a / b    # 3 (integer division)
let remainder = a % b   # 1
```

### Comparison Operators

```
let x = 10
let y = 20

let equal = x == y        # false
let not_equal = x != y    # true
let less_than = x < y     # true
let less_equal = x <= y   # true
let greater_than = x > y  # false
let greater_equal = x >= y # false
```

### Logical Operators

```
let a = true
let b = false

let logical_and = a and b  # false
let logical_or = a or b    # true
let logical_not = not a    # false
```

### String Operations

```
let first = "Hello"
let second = "World"

let combined = first + " " + second  # "Hello World"
let with_number = "Count: " + $42    # "Count: 42"
```

## Advanced Features

### Working with Secret Types

```
# Secret arithmetic
proc secure_calculation(a: secret int64, b: secret int64, c: int64): secret int64 =
  let secret_sum = a + b
  let mixed_operation = secret_sum * c  # Public value used with secret
  return mixed_operation

# Secret comparisons
proc secure_threshold(value: secret int64, threshold: int64): secret bool =
  return value > threshold

# Multiple secret operations
proc complex_secure_calc(
  secret_a: secret int64,
  secret_b: secret int64,
  public_factor: int64
): secret int64 =
  let temp1 = secret_a + secret_b
  let temp2 = secret_a * secret_b
  let result = (temp1 + temp2) * public_factor
  return result
```

### Error Handling (Planned)

```
# Try-catch blocks (future feature)
try:
  let result = risky_operation()
  print("Success: " + $result)
catch error:
  print("Error occurred: " + error.message)
```

### Pattern Matching (Planned)

```
# Match expressions (future feature)
let result = match status:
  Status.Active: "Currently active"
  Status.Inactive: "Not active"
  Status.Pending: "Waiting for approval"
  _: "Unknown status"
```

## Best Practices

### Naming Conventions

```
# Use snake_case for variables and functions
let user_name = "alice"
let max_retry_count = 5

proc calculate_total_cost(base_price: int64, tax_rate: int64): int64 =
  return base_price + (base_price * tax_rate / 100)

# Use PascalCase for types
type UserAccount = object
  user_id: int64
  account_balance: secret int64
```

### Type Safety

```
# Prefer explicit types for public interfaces
proc public_api(user_id: int64, amount: secret int64): bool =
  # Implementation
  return true

# Use type inference for local variables
proc internal_calculation() =
  let temp = 42  # Type inferred as int64
  let message = "Processing"  # Type inferred as string
```

### Secret Type Usage

```
# Clearly distinguish between public and secret data
proc process_transaction(
  public_user_id: int64,
  secret_amount: secret int64,
  public_currency: string
): secret bool =
  # Only secret operations on secret data
  let is_valid_amount = secret_amount > 0
  return is_valid_amount

# Avoid unnecessary secret wrapping
proc calculate_fee(amount: int64): int64 =  # Public calculation
  return amount * 5 / 100

proc apply_secret_fee(secret_amount: secret int64): secret int64 =
  let fee_rate = 5  # Public constant
  return secret_amount * fee_rate / 100  # Secret result
```

### Function Organization

```
# Small, focused functions
proc validate_age(age: int64): bool =
  return age >= 0 and age <= 150

proc validate_email(email: string): bool =
  # Simplified validation
  return email.length > 0

proc create_user(name: string, age: int64, email: string): Person =
  # Use validation functions
  if not validate_age(age):
    # Error handling (simplified)
    print("Invalid age")

  if not validate_email(email):
    print("Invalid email")

  return Person(
    name: name,
    age: age,
    email: email,
    is_active: true
  )
```

## Common Patterns

### Data Processing

```
proc process_user_data(user: Person): string =
  let age_category = if user.age < 18:
    "minor"
  elif user.age < 65:
    "adult"
  else:
    "senior"

  let status_text = if user.is_active: "active" else: "inactive"

  return user.name + " (" + age_category + ", " + status_text + ")"
```

### Secret Computation Patterns

```
# Secure comparison with public result indication
proc secure_age_check(secret_age: secret int64, min_age: int64): bool =
  let meets_requirement = secret_age >= min_age
  # In practice, this would use proper MPC reveal operations
  return true  # Simplified for syntax example

# Secure aggregation pattern
proc secure_sum(values: [secret int64; 5]): secret int64 =
  var total: secret int64 = 0
  for i in 0..5:
    # Note: Array indexing syntax may vary in implementation
    # This is a conceptual example
    total = total + values[i]
  return total
```

This syntax guide covers the current StoffelLang implementation and provides a foundation for understanding the language's structure and capabilities.
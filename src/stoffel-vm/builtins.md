# Built-in Functions

StoffelVM provides a set of built-in functions that are available to all StoffelLang programs. These functions handle common operations like I/O, array manipulation, and MPC-specific functionality.

## Console Output

### print

Outputs text to the console during program execution.

**Signature:**
```
print(message: string) -> nil
```

**Example:**
```python
def greet() -> nil:
    print("Hello, World!")
    print("Computation complete")
```

**Notes:**
- Output is displayed during VM execution
- Useful for debugging and progress tracking
- Does not reveal secret values (they remain masked)

## Array Operations

### array_push

Adds an element to the end of an array.

**Signature:**
```
array_push(array: [T], element: T) -> nil
```

**Example:**
```python
var numbers: [int64] = []
array_push(numbers, 10)
array_push(numbers, 20)
array_push(numbers, 30)
# numbers is now [10, 20, 30]
```

**Notes:**
- Uses **0-based indexing** (updated in recent versions)
- Modifies the array in place
- Works with both clear and secret element types

### array_len

Returns the length of an array.

**Signature:**
```
array_len(array: [T]) -> int64
```

**Example:**
```python
var items: [int64] = [1, 2, 3, 4, 5]
var count = array_len(items)  # count = 5
```

## ClientStore Operations

The `ClientStore` is a built-in singleton that provides access to client inputs in MPC computations. It acts as the bridge between external client data and the secure computation.

### ClientStore.get_number_clients

Returns the total number of clients participating in the MPC computation.

**Signature:**
```
ClientStore.get_number_clients() -> int64
```

**Returns:** A clear (non-secret) `int64` value representing the client count.

**Example:**
```python
main main() -> nil:
    var num_clients: int64 = ClientStore.get_number_clients()
    print("Clients connected")
```

**Notes:**
- Returns a **clear** (public) value, not a secret
- Can be assigned to regular variables
- Useful for dynamic iteration over client inputs

### ClientStore.take_share

Retrieves a secret share from a specific client at a given index.

**Signature:**
```
ClientStore.take_share(client_id: int64, share_index: int64) -> secret int64
```

**Parameters:**
- `client_id`: The ID of the client (0-indexed)
- `share_index`: The index of the share from that client (0-indexed)

**Returns:** A secret `int64` value.

**Example:**
```python
main main() -> nil:
    # Get first share from client 0
    secret var input1 = ClientStore.take_share(0, 0)

    # Get first share from client 1
    secret var input2 = ClientStore.take_share(1, 0)

    # Get second share from client 0
    secret var input3 = ClientStore.take_share(0, 1)
```

**Critical Constraint:**

Results from `ClientStore.take_share()` **must** be assigned to secret variables. The compiler enforces this requirement.

**Valid usage patterns:**
```python
# 1. Using 'secret var' keyword
secret var share1 = ClientStore.take_share(0, 0)

# 2. Using explicit secret type annotation
var share2: secret int64 = ClientStore.take_share(1, 0)

# 3. Reassigning to existing secret variable
secret var mutable_share: int64 = ClientStore.take_share(0, 0)
mutable_share = ClientStore.take_share(1, 0)  # Valid
```

**Invalid usage (compiler error):**
```python
# ERROR: Cannot assign take_share result to non-secret variable
var share: int64 = ClientStore.take_share(0, 0)

# ERROR: Implicit type doesn't make it secret
var share = ClientStore.take_share(0, 0)
```

## MPC-Specific Builtins

These functions are available when running in MPC mode and interact with the underlying protocol.

### Share Operations

When values are declared as `secret`, the VM automatically handles:
- **Secret sharing**: Splitting values into shares across parties
- **Share arithmetic**: Computing on shares using MPC protocols
- **Reconstruction**: Combining shares to produce final outputs

The programmer doesn't directly call share operations—they happen automatically when working with secret types.

### Protocol Integration

StoffelVM integrates with the HoneyBadger MPC protocol through internal hooks:

| Operation | Internal Function | Description |
|-----------|------------------|-------------|
| Addition | `mpc_add` | Adds two secret values |
| Subtraction | `mpc_sub` | Subtracts two secret values |
| Multiplication | `mpc_mul` | Multiplies using Beaver triples |
| Comparison | `mpc_cmp` | Compares two secret values |

These are invoked automatically by the VM when operating on secret types.

## Type Conversion Builtins

### int_to_string (Planned)

Convert an integer to its string representation.

```python
var num = 42
var text = int_to_string(num)  # "42"
```

### string_to_int (Planned)

Parse a string as an integer.

```python
var text = "123"
var num = string_to_int(text)  # 123
```

## Memory and Lifecycle

### Automatic Memory Management

StoffelVM manages memory automatically:
- Values are allocated on the stack or heap as needed
- Arrays grow dynamically with `array_push`
- Memory is reclaimed when values go out of scope

### Register Architecture

The VM uses a dual-register architecture:
- **Clear registers**: For public/non-secret values
- **Secret registers**: For MPC-protected values

Built-in functions automatically select the appropriate register set based on operand types.

## FFI Integration

StoffelVM supports calling external functions through Foreign Function Interface (FFI):

```rust
// Rust side: Register a custom builtin
vm.register_builtin("custom_hash", |args| {
    // Implementation
});
```

```python
# StoffelLang side: Call the custom builtin
var result = custom_hash(data)
```

See the [Architecture - FFI](../architecture/subsections/foreignfunctioninterface.md) section for details on implementing custom builtins.

## Summary Table

| Function | Input Types | Return Type | Description |
|----------|-------------|-------------|-------------|
| `print` | string | nil | Console output |
| `array_push` | [T], T | nil | Add element to array |
| `array_len` | [T] | int64 | Get array length |
| `ClientStore.get_number_clients` | - | int64 (clear) | Get client count |
| `ClientStore.take_share` | int64, int64 | secret int64 | Get client share |

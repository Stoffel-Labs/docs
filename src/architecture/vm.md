# VM Architecture Details

This section covers the detailed architectural design of StoffelVM. For implementation details and current status, see [StoffelVM Implementation Details](../stoffel-vm/implementation.md).

## Register Architecture

StoffelVM uses a register-based architecture with two distinct register spaces:

### Clear Registers
- Store public/non-secret values
- Direct CPU register mapping for performance
- Standard arithmetic and logical operations
- No cryptographic overhead

### Secret Registers
- Store secret-shared values for MPC
- Protocol-agnostic secret handling
- Automatic secret sharing and reconstruction
- MPC-optimized operations

## Memory Model

### Object Store
- Dynamic object allocation with reference counting
- Key-value mappings for flexible data structures
- Garbage collection integration points

### Array Store
- Contiguous memory layout for arrays
- Dynamic resizing capabilities
- Index bounds checking

### Stack Management
- Function call activation records
- Parameter passing via argument stack
- Local variable storage

## Instruction Pipeline

### Fetch-Decode-Execute Cycle
1. **Instruction Fetch**: Retrieve next instruction from program counter
2. **Decode**: Parse instruction opcode and operands
3. **Execute**: Perform operation with register/memory access
4. **Writeback**: Store result in destination register

### Hook Integration Points
- Pre-instruction hooks for debugging
- Post-instruction hooks for monitoring
- Register access hooks for MPC protocol integration
- Memory operation hooks for garbage collection

## Type System Integration

### Value Types
The VM supports a rich type system with runtime type information:
- Primitive types (integers, floats, booleans, strings)
- Complex types (objects, arrays, closures)
- Foreign objects for host language integration

### Type Safety
- Runtime type checking for operations
- Type coercion rules for mixed operations
- Error handling for type mismatches

## Closure System

### Lexical Scoping
- True lexical scoping with upvalue capture
- Closure creation with environment capture
- Upvalue sharing between closures

### Function Calls
- Dynamic function dispatch
- Parameter binding and local variable allocation
- Return value handling

## Protocol Integration

### MPC Protocol Interface
- Abstract protocol operations for secret sharing
- Reveal operations for secret-to-clear transitions
- Communication round optimization

### Clear/Secret Transitions
- Automatic hiding (clear → secret) on register moves
- Explicit revealing (secret → clear) operations
- Type preservation during transitions

This architectural design enables efficient MPC computation while maintaining the flexibility to support different protocols and optimization strategies.

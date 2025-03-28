# Architecture

Stoffel VM is a register based virtual machine with two sets of registers. Clear registers for manipulating non-secret values. Secret registers are used for manipulating secret values.

## Technical Overview

### [Virtual Machine Architecture](./subsections/virtualmachine.md)
- What type of VM is stoffel
- Clear vs Secret values

### [Instruction Set](./subsections/instructionset.md)
- Complete reference of supported VM instructions
- Opcode specifications and behavior
- Optimization opportunities

### [Builtin Types](./subsections/builtintypes.md)
- Overview of core data types (numbers, strings, arrays, etc.)
- Type conversion and manipulation
- Memory representation and optimization

### [Activation Records](./subsections/activationrecords.md)
- Call stack management and function invocation
- Local variable scoping and lifetime
- Optimizing stack frame allocation

### [VM Functions](./subsections/vmfunctions.md)
- Virtual machine architecture overview
- Execution model and stack management
- Error handling

### [Closures Overview](./subsections/closures.md)
- Lexical scoping and variable capture
- Implementation details and memory management

### [Foreign Function Interface](./subsections/foreignfunctioninterface.md)
- Integrating with external libraries and systems
- Data marshalling and type conversion
- Performance considerations for FFI calls

### [Builtin Methods](./subsections/builtinmethods.md)
- Standard library functions and utilities
- Common operations for each data type

### [Runtime Hooks](./subsections/runtimehooks.md)
- Extension points for monitoring and customization
- Performance profiling and instrumentation
- Debugging facilities

## Why a Register Machine?

The choice of a register-based architecture over a stack-based design was driven by several key factors:

1. **Parallelization Opportunities**
   - Register machines allow for easier identification of independent instructions
   - Multiple instructions can be executed in parallel, reducing overall execution time
   - Better suited for modern hardware architectures

2. **Communication Efficiency**
   - Reduced number of memory access operations
   - Fewer rounds of communication in Multi-Party Computation (MPC) contexts
   - More efficient instruction encoding

3. **Optimization Potential**
   - Direct access to operands enables better optimization strategies
   - Easier to implement specialized instructions
   - More straightforward analysis of data flow

## Why dedicated clear and secret registers

1. **Implicit reveal and hide**
   - Having dedicated registers for secret and clear values allows us to implicitly reveal and hide values as they're moved between registers.
   - Separation of registers allows for optimizations to be applied specifically to clear or secret operations.
   - Avoids having to track the type of the virtual register during runtime as values may become secret shared or reveal through the course of execution.
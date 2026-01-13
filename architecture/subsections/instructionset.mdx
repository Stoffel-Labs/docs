# Introduction to Stoffel's Instruction Set

This page contains the rationale and overview of the specialized instruction set that is currently supported by Stoffel's runtime.

## Rationale

We developed Stoffel's custom instruction set primarily to address the unique requirements of Multi-Party Computation (MPC). Our VM needed to efficiently handle both clear and secret value domains while providing just enough expressiveness for both types of computation. By deliberately keeping the instruction set minimal, we gained significant advantages: better performance optimization, easier identification of inefficient operations during MPC execution, and most importantly, a more straightforward path to verifying the VM's security properties compared to adapting an existing architecture.

## Comprehensive Overview

The runtime's instruction set is designed to support both clear and secret values. When describing an instruction they should follow a consistent format where an opcode is followed by its operands in parentheses. In other words, the way to read and write the instructions is as follows: `OPCODE(OPERAND1, OPERAND2, ...)`.

Instructions generally fall into four distinct categories.

1. [Memory Operations](#memory-operations): Manage the flow of data between registers and memory.

2. [Arithmetic Operations](#arithmetic-operations): Perform fundamental mathematical operations.

3. [Bitwise Operations](#bitwise-operations): Handle low level binary manipulation.

4. [Control Flow](#control-flow): Direct the program execution path.

Most instructions follow a destination-first convention (e.g: `ADD(destination, source1, source2)`), making it obvious where results will be stored. Regular operands are used for most operations, with immediate values supported via the `LDI` instruction. Function calls use `CALL` and `PUSHARG` for passing arguments, with `RET` handling return values.

The format prioritizes clarity while avoiding unnecessary complexity that could unexpectedly compromise the runtime's security properties

## Memory Operations

- `LD(dest_reg, stack_offset)`:
  Loads a value from the stack at the specified offset into the destination register.
  - `dest_reg`: The register where the loaded value will be stored
  - `stack_offset`: The position in the stack relative to the current frame pointer from which to load the value


- `LDI(dest_reg, value)`:
  Loads an immediate (constant) value directly into the specified register.
  - `dest_reg`: The register where the immediate value will be stored
  - `value`: The actual constant value to be loaded


- `MOV(dest_reg, src_reg)`:
  Copies the value from the source register to the destination register.
  - `dest_reg`: The register that will receive the copied value
  - `src_reg`: The register containing the value to be copied


- `PUSHARG(reg)`:
  Pushes the value in the specified register onto the argument stack.
  - `reg`: The register containing the value to be pushed as a function argument

## Arithmetic Operations

- `ADD(dest_reg, src1_reg, src2_reg)`:
  Adds two values and stores the result.
  - `dest_reg`: The register where the sum will be stored
  - `src1_reg`: The register containing the first operand
  - `src2_reg`: The register containing the second operand


- `SUB(dest_reg, src1_reg, src2_reg)`:
  Subtracts the second value from the first value.
  - `dest_reg`: The register where the difference will be stored
  - `src1_reg`: The register containing the minuend (value being subtracted from)
  - `src2_reg`: The register containing the subtrahend (value being subtracted)


- `MUL(dest_reg, src1_reg, src2_reg)`:
  Multiplies two values and stores the product.
  - `dest_reg`: The register where the product will be stored
  - `src1_reg`: The register containing the first factor
  - `src2_reg`: The register containing the second factor


- `DIV(dest_reg, src1_reg, src2_reg)`:
  Divides the first value by the second value.
  - `dest_reg`: The register where the quotient will be stored
  - `src1_reg`: The register containing the dividend (value being divided)
  - `src2_reg`: The register containing the divisor (value dividing by)


- `MOD(dest_reg, src1_reg, src2_reg)`:
  Calculates the remainder when dividing the first value by the second value.
  - `dest_reg`: The register where the remainder will be stored
  - `src1_reg`: The register containing the dividend (value being divided)
  - `src2_reg`: The register containing the divisor (value dividing by)

## Bitwise Operations

- `AND(dest_reg, src1_reg, src2_reg)`:
  Performs a bitwise AND operation (result bit is 1 only if both input bits are 1).
  - `dest_reg`: The register where the result will be stored
  - `src1_reg`: The register containing the first operand
  - `src2_reg`: The register containing the second operand


- `OR(dest_reg, src1_reg, src2_reg)`:
  Performs a bitwise OR operation (result bit is 1 if either input bit is 1).
  - `dest_reg`: The register where the result will be stored
  - `src1_reg`: The register containing the first operand
  - `src2_reg`: The register containing the second operand


- `XOR(dest_reg, src1_reg, src2_reg)`:
  Performs a bitwise XOR operation (result bit is 1 if exactly one input bit is 1).
  - `dest_reg`: The register where the result will be stored
  - `src1_reg`: The register containing the first operand
  - `src2_reg`: The register containing the second operand


- `NOT(dest_reg, src_reg)`:
  Performs a bitwise complement operation (flips all bits).
  - `dest_reg`: The register where the result will be stored
  - `src_reg`: The register containing the value to be complemented


- `SHL(dest_reg, src_reg, amount_reg)`:
  Shifts all bits in a value to the left (equivalent to multiplying by powers of 2).
  - `dest_reg`: The register where the shifted result will be stored
  - `src_reg`: The register containing the value to be shifted
  - `amount_reg`: The register containing the number of positions to shift


- `SHR(dest_reg, src_reg, amount_reg)`:
  Shifts all bits in a value to the right (equivalent to dividing by powers of 2).
  - `dest_reg`: The register where the shifted result will be stored
  - `src_reg`: The register containing the value to be shifted
  - `amount_reg`: The register containing the number of positions to shift


## Control Flow

- `JMP(label)`:
  Unconditionally changes the program counter to point to the specified label.
  - `label`: The target instruction address or symbolic label where execution will continue


- `JMPEQ(label)`:
  Conditionally jumps if the compare flag indicates equality (zero).
  - `label`: The target symbolic label to jump to if condition is met


- `JMPNEQ(label)`:
  Conditionally jumps if the compare flag indicates inequality (non-zero).
  - `label`: The target symbolic label to jump to if condition is met


- `CMP(reg1, reg2)`:
  Compares two values and sets the internal compare flag based on their relationship.
  - `reg1`: The register containing the first value to compare
    - `reg2`: The register containing the second value to compare


- `CALL(function_name)`:
  Saves the current execution context and transfers control to the named function.
   - `function_name`: The name or address of the function to be called


- `RET(reg)`:
  Restores the previous execution context and provides a return value.
  - `reg`: The register containing the value to be returned to the caller
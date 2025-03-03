# Architecture

Stoffel VM is a register based virtual machine with two sets of registers. Clear registers for manipulating non-secret values. Secret registers are used for manipulating secret values.

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
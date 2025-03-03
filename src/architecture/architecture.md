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

## 
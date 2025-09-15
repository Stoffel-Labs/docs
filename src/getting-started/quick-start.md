# Quick Start

Get up and running with Stoffel in just a few minutes! This guide will walk you through creating your first privacy-preserving application using Multi-Party Computation.

## Prerequisites

Make sure you have Stoffel installed on your system. If not, follow the [Installation](./installation.md) guide first.

```bash
# Verify Stoffel is installed
stoffel --version
```

## 5-Minute MPC Application

Let's create a simple secure addition application where two parties can compute the sum of their private numbers without revealing them to each other.

### Step 1: Create a New Project

```bash
# Create a new Stoffel project
stoffel init secure-addition

# Navigate to the project directory
cd secure-addition
```

This creates a basic project structure:
```
secure-addition/
├── Stoffel.toml          # Project configuration
├── src/
│   └── main.stfl         # Main StoffelLang source file
├── tests/
└── README.md
```

### Step 2: Write Your First StoffelLang Program

Open `src/main.stfl` and replace the contents with:

```javascript
// Secure addition function
fn secure_add(a: secret i32, b: secret i32) -> secret i32 {
    return a + b;
}

// Main function - entry point for execution
fn main() {
    // These values would normally come from different parties
    let secret_value_a = secret(25);
    let secret_value_b = secret(17);

    // Perform secure computation
    let secure_result = secure_add(secret_value_a, secret_value_b);

    // Reveal the result (only the final result, not the inputs)
    let public_result = reveal(secure_result);

    // Print the result
    println("Secure addition result: {}", public_result);
}
```

### Step 3: Compile Your Program

```bash
# Compile the StoffelLang program to VM bytecode
stoffel compile src/main.stfl --binary --output secure-addition.stfbin
```

This will:
- Parse and compile your StoffelLang code
- Generate optimized VM bytecode
- Create a compiled `.stfbin` file ready for execution

You should see output like:
```
Compiling src/main.stfl...
Compilation successful!
Generating VM-compatible binary...
Binary saved to secure-addition.stfbin
```

### Step 4: Run Your Application

```bash
# Execute the compiled program using StoffelVM
stoffel-run secure-addition.stfbin main
```

This runs your secure computation and you should see:
```
Program returned: Unit
```

The program executes successfully! For more detailed execution tracing, you can use debug flags:

```bash
# Trace instruction execution
stoffel-run secure-addition.stfbin main --trace-instr

# Trace register operations
stoffel-run secure-addition.stfbin main --trace-regs

# Trace function calls and stack operations
stoffel-run secure-addition.stfbin main --trace-stack
```

### Step 5: Development Workflow

> **Note**: The integrated `stoffel run` command is currently under development. For now, use this workflow:

```bash
# 1. Edit your .stfl file
# 2. Recompile when you make changes
stoffel compile src/main.stfl --binary --output secure-addition.stfbin

# 3. Test the changes
stoffel-run secure-addition.stfbin main

# 4. For debugging, enable tracing
stoffel-run secure-addition.stfbin main --trace-instr --trace-regs
```

## Understanding What Happened

### The Magic of MPC

In your secure addition example:

1. **Secret Sharing**: Your inputs (25 and 17) were automatically split into shares
2. **Distributed Computation**: Each party computed on shares without seeing the original values
3. **Result Reconstruction**: The final result (42) was reconstructed from the output shares

```
Party 1: Receives shares [8, 23] → Computes 8 + 23 = 31
Party 2: Receives shares [5, 12] → Computes 5 + 12 = 17
Party 3: Receives shares [12, -18] → Computes 12 + (-18) = -6
...
Result: Reconstruct 31 + 17 + (-6) + ... = 42
```

No single party ever saw your original values (25 and 17)!

### StoffelLang Features

Your simple program demonstrated several key features:

- **Secret Types**: `secret i32` for private data
- **Automatic Operations**: `+` works on secret values
- **Reveal Operations**: `reveal()` to make results public
- **Built-in Functions**: `println()` for output

## Next Steps

### Try Different Examples

Experiment with different StoffelLang programs by modifying `src/main.stfl`:

```bash
# After editing, recompile and run
stoffel compile src/main.stfl --binary --output example.stfbin
stoffel-run example.stfbin main
```

### Future Features

> **Coming Soon**: The following features are currently under development:
>
> - **Templates**: `stoffel init --template <name>` for common use cases
> - **Python SDK Integration**: Seamless Python bindings
> - **Development Server**: `stoffel dev` with hot reloading and web interface
> - **Advanced CLI**: Testing, deployment, and protocol management commands

## Common Commands

Here are the essential commands you'll use regularly:

```bash
# Project creation
stoffel init <name>                 # Create new project structure

# Compilation
stoffel compile <source.stfl>       # Compile to bytecode
stoffel compile <source.stfl> --binary --output <file.stfbin>

# Compilation options
--binary            # Generate VM-compatible binary format
--output/-o         # Specify output file path
--print-ir          # Show intermediate representations
-O0 to -O3          # Optimization levels (0=none, 3=maximum)
--disassemble       # Disassemble compiled binary

# Execution (using StoffelVM)
stoffel-run <program.stfbin> [entry_function] [flags]

# Execution debugging flags:
--trace-instr       # Trace instructions before/after execution
--trace-regs        # Trace register reads/writes
--trace-stack       # Trace function calls and stack operations

# Help and information
stoffel --help                      # Show CLI help
stoffel compile --help              # Show compiler help
stoffel-run --help                  # Show VM runner help
```

> **Development Note**: Advanced CLI features like `stoffel run`, `stoffel dev`, `stoffel test`, and `stoffel deploy` are currently under development. The core workflow using `stoffel compile` and `stoffel-run` is fully functional.

## What's Next?

Now that you've created your first MPC application:

1. **[Basic Usage](./basic-usage.md)**: Learn all the essential Stoffel CLI commands
2. **[Your First MPC Project](./first-project.md)**: Build a more complex privacy-preserving application
3. **[StoffelLang Overview](../stoffel-lang/overview.md)**: Deep dive into the programming language
4. **[Python SDK](../python-sdk/overview.md)**: Integrate Stoffel with Python applications

## Troubleshooting

### Compilation Errors

```bash
# Check detailed compiler output
stoffel compile src/main.stfl --print-ir --binary --output debug.stfbin

# The --print-ir flag shows intermediate representations including:
# - Generated bytecode
# - Constants and labels
# - Function chunks
```

### Runtime Errors

```bash
# Use tracing flags to debug execution
stoffel-run program.stfbin main --trace-instr --trace-regs --trace-stack

# This provides detailed execution traces showing:
# - Instruction execution order
# - Register read/write operations
# - Function call stack operations
```

### Common Issues

**"Error loading binary"**: Ensure the `.stfbin` file was compiled successfully and the path is correct.

**"Execution error"**: Check that the entry function exists and has the correct signature using `--trace-instr` for debugging.

## Example Variations

Try these variations of the secure addition example:

### Secure Comparison

```javascript
fn secure_compare(a: secret i32, b: secret i32) -> secret bool {
    return a > b;
}

fn main() {
    let alice_value = secret(75);
    let bob_value = secret(68);

    let alice_wins = secure_compare(alice_value, bob_value);
    let result = reveal(alice_wins);

    println("Alice has higher value: {}", result);
}
```

### Secure Average

```javascript
fn secure_average(values: secret [i32; 3]) -> secret i32 {
    let sum = secret(0);
    for value in values {
        sum = sum + value;
    }
    return sum / secret(3);
}

fn main() {
    let party_values = secret([85, 92, 78]);
    let average = secure_average(party_values);
    let result = reveal(average);

    println("Average score: {}", result);
}
```

You're now ready to build privacy-preserving applications with Stoffel! The framework handles all the complex cryptography while you focus on your application logic.

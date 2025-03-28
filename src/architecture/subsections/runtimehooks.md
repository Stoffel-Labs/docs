# Hooks and Debugging in Stoffel

This page describes Stoffel's hook system, which provides powerful instrumentation capabilities for monitoring and debugging VM execution.

## Rationale

The hook system enables comprehensive monitoring of the VM's internal operations without modifying the core execution logic. By providing event-based callbacks at various points in program execution, hooks allow for powerful debugging, tracing, and analysis capabilities. This design separates the core VM logic from monitoring concerns, making the system more maintainable while providing the visibility needed for development and troubleshooting.

## Comprehensive Overview

Stoffel's hook system is based on an event-driven architecture where various VM operations trigger events that can be captured by registered hooks. Each hook consists of a predicate function that determines when the hook should fire and a callback function that executes when the hook is triggered.

The hook system allows for monitoring of instruction execution, register operations, variable access, object/array manipulations, function calls, and other VM operations. Hooks can be enabled, disabled, and prioritized, providing flexible control over the monitoring process.

## Hook Events

Hooks are triggered by various events during VM execution:

- `BeforeInstructionExecute(Instruction)`:
  Fired before an instruction is executed.
  - Provides the instruction about to be executed
  - Useful for tracing program flow

- `AfterInstructionExecute(Instruction)`:
  Fired after an instruction is executed.
  - Provides the instruction that was just executed
  - Useful for analyzing the effects of instructions

- `RegisterRead(usize, Value)`:
  Fired when a register is read.
  - Includes the register index and its current value
  - Helps track data flow through registers

- `RegisterWrite(usize, Value, Value)`:
  Fired when a register is written to.
  - Includes the register index, old value, and new value
  - Useful for tracking value changes

- `VariableRead(String, Value)`:
  Fired when a local variable is read.
  - Includes the variable name and its value
  - Helps monitor variable usage

- `VariableWrite(String, Value, Value)`:
  Fired when a local variable is written to.
  - Includes the variable name, old value, and new value
  - Useful for tracking variable modifications

- `UpvalueRead(String, Value)`:
  Fired when a closure upvalue is read.
  - Includes the upvalue name and its value
  - Helps debug closure behavior

- `UpvalueWrite(String, Value, Value)`:
  Fired when a closure upvalue is written to.
  - Includes the upvalue name, old value, and new value
  - Useful for tracking closure state changes

- `ObjectFieldRead(usize, Value, Value)`:
  Fired when an object field is read.
  - Includes the object ID, field key, and value
  - Helps track object data access

- `ObjectFieldWrite(usize, Value, Value, Value)`:
  Fired when an object field is written to.
  - Includes the object ID, field key, old value, and new value
  - Useful for monitoring object modifications

- `ArrayElementRead(usize, Value, Value)`:
  Fired when an array element is read.
  - Includes the array ID, element index, and value
  - Helps track array data access

- `ArrayElementWrite(usize, Value, Value, Value)`:
  Fired when an array element is written to.
  - Includes the array ID, element index, old value, and new value
  - Useful for monitoring array modifications

- `BeforeFunctionCall(Value, Vec<Value>)`:
  Fired before a function is called.
  - Includes the function and its arguments
  - Helps track function invocations

- `AfterFunctionCall(Value, Value)`:
  Fired after a function returns.
  - Includes the function and its return value
  - Useful for analyzing function results

- `ClosureCreated(String, Vec<Upvalue>)`:
  Fired when a closure is created.
  - Includes the function name and captured upvalues
  - Helps debug closure creation

- `StackPush(Value)`:
  Fired when a value is pushed onto the stack.
  - Includes the pushed value
  - Helps track stack operations

- `StackPop(Value)`:
  Fired when a value is popped from the stack.
  - Includes the popped value
  - Useful for monitoring stack usage

## Hook Context

When a hook is triggered, it receives a context object providing safe access to the VM state:

- `current_activation_record()`: Gets the current activation record
- `get_compare_flag()`: Gets the current comparison flag
- `get_register_value(reg_idx)`: Gets a register's current value
- `get_current_instruction()`: Gets the current instruction pointer
- `get_function_name()`: Gets the name of the current function
- `get_call_depth()`: Gets the current call stack depth
- `get_instruction_at(function_name, index)`: Gets an instruction from a function

These methods provide controlled access to VM state without exposing mutable references that could compromise VM integrity.

## Hook Management

Hooks are managed through the `HookManager`, which provides methods for registering, unregistering, enabling, and disabling hooks:

- `register_hook(predicate, callback, priority)`:
  Registers a new hook with the specified predicate, callback, and priority.
  - Returns a unique hook ID for later reference
  - Higher priority hooks execute before lower priority ones

- `unregister_hook(hook_id)`:
  Removes a hook from the system.
  - Returns a boolean indicating success
  - Allows cleanup of hooks when no longer needed

- `enable_hook(hook_id)`:
  Enables a previously disabled hook.
  - Returns a boolean indicating success
  - Allows selective activation of hooks

- `disable_hook(hook_id)`:
  Temporarily disables a hook without removing it.
  - Returns a boolean indicating success
  - Useful for conditionally turning off hooks

- `trigger(event, vm_state)`:
  Triggers all matching hooks for an event.
  - Called internally by the VM when events occur
  - Executes each matching hook's callback with the provided VM state

## Usage Examples

Hooks can be used for various debugging and monitoring purposes, as demonstrated in the factorial function test:

1. **Instruction Tracing**:
    ```rust
    vm.register_hook(
       |event| matches!(event, HookEvent::BeforeInstructionExecute(_)),
       move |event, ctx| {
           if let HookEvent::BeforeInstructionExecute(instruction) = event {
               println!("EXEC: {:?}", instruction);
           }
           Ok(())
       },
       100,
    );
    ```

2. **Comparison Monitoring**:
    ```rust
    vm.register_hook(
       |event| matches!(event, HookEvent::AfterInstructionExecute(Instruction::CMP(_, _))),
       move |event, ctx| {
           if let HookEvent::AfterInstructionExecute(Instruction::CMP(reg1, reg2)) = event {
               println!("CMP r{} r{} = {}", reg1, reg2, ctx.get_compare_flag().unwrap_or(0));
           }
           Ok(())
       },
       90,
    );
    ```

3. **Function Call Tracing**:
   ```rust
   vm.register_hook(
       |event| matches!(event, HookEvent::BeforeFunctionCall(_, _)),
       move |event, ctx| {
           if let HookEvent::BeforeFunctionCall(_, args) = event {
               println!("CALL with args: {:?}", args);
           }
           Ok(())
       },
       80,
   );
   ```

4. **Jump Decision Tracking**:
   ```rust
   vm.register_hook(
       |event| matches!(event, HookEvent::BeforeInstructionExecute(Instruction::JMPEQ(_))),
       move |event, ctx| {
           if let HookEvent::BeforeInstructionExecute(Instruction::JMPEQ(label)) = event {
               println!("JUMP to {} will {}", label, 
                       if ctx.get_compare_flag() == Some(0) { "HAPPEN" } else { "NOT HAPPEN" });
           }
           Ok(())
       },
       70,
   );
   ```

These examples demonstrate how hooks can provide detailed visibility into VM execution, helping developers understand program behavior and diagnose issues.
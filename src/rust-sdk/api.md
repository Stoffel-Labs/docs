# API Reference

## Stoffel Builder

The main entry point for all SDK operations.

### Compilation Methods

```rust
// Compile from source string
Stoffel::compile(source: &str) -> Result<StoffelBuilder>

// Compile from file
Stoffel::compile_file(path: &str) -> Result<StoffelBuilder>

// Load pre-compiled bytecode
Stoffel::load(bytecode: Vec<u8>) -> Result<StoffelBuilder>
```

### Configuration Methods

```rust
impl StoffelBuilder {
    // MPC party count (minimum 4 for HoneyBadger)
    fn parties(self, n: usize) -> Self

    // Fault tolerance threshold (default: 1)
    fn threshold(self, t: usize) -> Self

    // Unique computation instance ID
    fn instance_id(self, id: u64) -> Self

    // MPC protocol selection
    fn protocol(self, protocol: ProtocolType) -> Self

    // Secret sharing scheme
    fn share_type(self, share_type: ShareType) -> Self

    // Enable compiler optimization
    fn optimize(self, enabled: bool) -> Self

    // Load network config from TOML file
    fn network_config_file(self, path: &str) -> Result<Self>

    // Set network config programmatically
    fn network_config(self, config: NetworkConfig) -> Self

    // Build the runtime
    fn build(self) -> Result<StoffelRuntime>

    // Quick local execution (skips MPC setup)
    fn execute_local(self) -> Result<Value>
}
```

### Types

```rust
pub enum ProtocolType {
    HoneyBadger,  // Currently the only supported protocol
}

pub enum ShareType {
    Robust,      // Reed-Solomon error correction (default)
    NonRobust,   // Standard Shamir secret sharing
}
```

## StoffelRuntime

Created by `StoffelBuilder::build()`, provides access to program and MPC participants.

```rust
impl StoffelRuntime {
    // Access the compiled program
    fn program(&self) -> &Program

    // Get MPC configuration
    fn mpc_config(&self) -> Option<(usize, usize, u64)>  // (parties, threshold, instance_id)

    // Get protocol type
    fn protocol_type(&self) -> ProtocolType

    // Get share type
    fn share_type(&self) -> ShareType

    // Create MPC client builder
    fn client(&self, id: u64) -> MPCClientBuilder

    // Create MPC server builder
    fn server(&self, id: usize) -> MPCServerBuilder

    // Create MPC node builder (combined client + server)
    fn node(&self, id: usize) -> MPCNodeBuilder
}
```

## Program

Pure bytecode container with execution methods.

```rust
impl Program {
    // Get raw bytecode
    fn bytecode(&self) -> &[u8]

    // Save bytecode to file
    fn save(&self, path: &str) -> Result<()>

    // Execute main function locally (no MPC)
    fn execute_local(&self) -> Result<Value>

    // Execute specific function locally
    fn execute_local_function(&self, name: &str) -> Result<Value>

    // Execute function with arguments
    fn execute_local_with_args(&self, name: &str, args: Vec<Value>) -> Result<Value>

    // List available functions
    fn list_functions(&self) -> Result<Vec<FunctionInfo>>
}

pub struct FunctionInfo {
    pub name: String,
    pub parameters: Vec<String>,
    pub register_count: usize,
}
```

## MPCClient

Input provider that does not participate in computation.

### Builder

```rust
impl MPCClientBuilder {
    // Set secret inputs
    fn with_inputs(self, inputs: Vec<i64>) -> Self

    // Build the client
    fn build(self) -> Result<MPCClient>
}
```

### Methods

```rust
impl MPCClient {
    // Add server to connect to
    fn add_server(&mut self, id: usize, addr: SocketAddr)

    // Connect to all configured servers
    async fn connect_to_servers(&mut self) -> Result<()>

    // Send secret-shared inputs to servers
    async fn send_inputs(&mut self) -> Result<()>

    // Receive and reconstruct outputs
    async fn receive_outputs(&mut self) -> Result<Value>
}
```

## MPCServer

Compute node that performs MPC operations.

### Builder

```rust
impl MPCServerBuilder {
    // Configure preprocessing material
    fn with_preprocessing(self, triples: usize, random_shares: usize) -> Self

    // Build the server
    fn build(self) -> Result<MPCServer>
}
```

### Methods

```rust
impl MPCServer {
    // Add peer server
    fn add_peer(&mut self, id: usize, addr: SocketAddr)

    // Start listening for connections
    async fn bind_and_listen(&mut self, addr: SocketAddr) -> Result<()>

    // Initialize the MPC node
    fn initialize_node(&mut self) -> Result<()>

    // Spawn message processor
    async fn spawn_message_processor(&mut self, receiver: Receiver<Message>, id: usize) -> Result<()>

    // Connect to peer servers
    async fn connect_to_peers(&mut self) -> Result<()>

    // Load program bytecode
    fn load_bytecode(&mut self, bytecode: &[u8]) -> Result<()>
}
```

## MPCNode

Combined client and server for peer-to-peer MPC.

### Builder

```rust
impl MPCNodeBuilder {
    // Set secret inputs
    fn with_inputs(self, inputs: Vec<i64>) -> Self

    // Configure preprocessing material
    fn with_preprocessing(self, triples: usize, random_shares: usize) -> Self

    // Build the node
    fn build(self) -> Result<MPCNode>
}
```

## StoffelClient (MPCaaS)

High-level client API for app developers. Handles connection, input submission, and result retrieval.

### Builder

```rust
impl StoffelClientBuilder {
    // Set server addresses to connect to
    fn with_servers(self, servers: &[&str]) -> Self

    // Set client ID (auto-generated if not specified)
    fn client_id(self, id: u64) -> Self

    // Set connection timeout
    fn connection_timeout(self, duration: Duration) -> Self

    // Set computation timeout
    fn computation_timeout(self, duration: Duration) -> Self

    // Connect to the MPC network
    async fn connect(self) -> Result<StoffelClient>
}
```

### Methods

```rust
impl StoffelClient {
    // Create a new builder
    fn builder() -> StoffelClientBuilder

    // Submit inputs and wait for result (blocking)
    async fn run(&self, inputs: &[i64]) -> Result<i64>

    // Submit inputs (non-blocking)
    async fn submit(&self, inputs: &[i64]) -> Result<ComputationHandle>

    // Get current client state
    fn state(&self) -> ClientState

    // Disconnect from servers
    async fn disconnect(self) -> Result<()>
}

impl ComputationHandle {
    // Wait for computation result
    async fn await_result(self) -> Result<i64>

    // Check if computation is complete
    fn is_complete(&self) -> bool

    // Cancel the computation
    async fn cancel(self) -> Result<()>
}
```

### Client States

```rust
pub enum ClientState {
    // Connected to servers, ready to submit
    Connected,

    // Currently sending input shares
    Submitting,

    // Waiting for computation result
    Computing,

    // Session ended
    Disconnected,
}
```

## StoffelServer (MPCaaS)

High-level server API for infrastructure operators. Manages peer connections and computation.

### Builder

```rust
impl StoffelServerBuilder {
    // Set bind address for incoming connections
    fn bind(self, address: &str) -> Self

    // Set peer server addresses
    fn with_peers(self, peers: &[(usize, &str)]) -> Self

    // Set the compiled program to execute
    fn with_program(self, program: Program) -> Self

    // Configure preprocessing parameters
    fn with_preprocessing(self, n_triples: usize, n_random_shares: usize) -> Self

    // Set instance ID (must match across all servers)
    fn with_instance_id(self, id: u64) -> Self

    // Set preprocessing start time (must match across all servers)
    fn with_preprocessing_start_time(self, epoch: u64) -> Self

    // Build the server
    fn build(self) -> Result<StoffelServer>
}

// Entry point
Stoffel::server(party_id: usize) -> StoffelServerBuilder
```

### Methods

```rust
impl StoffelServer {
    // Start the QUIC listener
    async fn start(&self) -> Result<()>

    // Connect to all peer servers (establish full mesh)
    async fn connect_to_peers(&self) -> Result<()>

    // Run preprocessing phase
    async fn run_preprocessing(&self) -> Result<()>

    // Handle a single computation session
    async fn run_once(&self) -> Result<()>

    // Run indefinitely, handling multiple sessions
    async fn run_forever(&self) -> Result<()>

    // Get current server state
    fn state(&self) -> ServerState

    // Graceful shutdown
    async fn shutdown(self) -> Result<()>
}
```

### Server States

```rust
pub enum ServerState {
    // Just created, not started
    Initialized,

    // Binding to port
    Starting,

    // Establishing peer connections
    ConnectingPeers,

    // Generating preprocessing material
    Preprocessing,

    // Ready to accept clients
    Ready,

    // Actively computing
    Computing,

    // Shutting down
    ShuttingDown,
}
```

### Configuration Synchronization

All servers in an MPC cluster must agree on these parameters:

```rust
// These values MUST be identical across all servers
let instance_id: u64 = 12345;
let n_parties: usize = 5;
let threshold: usize = 1;

// Start preprocessing at the same wall-clock time
let preprocessing_start_epoch = SystemTime::now()
    .duration_since(UNIX_EPOCH)?
    .as_secs() + 20;  // 20 seconds in future
```

**Failure to synchronize causes:**
- `instance_id` mismatch: Parties won't recognize each other
- `n_parties` mismatch: Protocol messages misrouted
- `preprocessing_start_epoch` mismatch: Preprocessing fails

## Error Types

```rust
pub enum Error {
    // StoffelLang compilation failures
    CompilationError(String),

    // VM execution errors
    RuntimeError(String),

    // MPC protocol errors
    MPCError(String),

    // File/network IO errors
    IoError(std::io::Error),

    // Invalid parameters
    InvalidInput(String),

    // Missing function
    FunctionNotFound(String),

    // Network communication errors
    Network(String),

    // Configuration validation failures
    Configuration(String),

    // MPC preprocessing errors
    Preprocessing(String),

    // MPC computation errors
    Computation(String),

    // Generic error
    Other(String),
}

pub type Result<T> = std::result::Result<T, Error>;
```

## Value Type

VM execution results:

```rust
pub enum Value {
    I64(i64),
    I32(i32),
    I16(i16),
    I8(i8),
    U64(u64),
    U32(u32),
    U16(u16),
    U8(u8),
    Float(i64),      // Fixed-point representation
    Bool(bool),
    String(String),
    Unit,            // Nil/void
    Object(usize),   // Reference to object
    Array(usize),    // Reference to array
    Share(ShareType, Vec<u8>),  // Secret-shared value
}
```

## Prelude

For convenience, import all common types:

```rust
use stoffel_rust_sdk::prelude::*;

// Includes:
// - Stoffel, StoffelRuntime, Program
// - MPCClient, MPCServer, MPCNode
// - ProtocolType, ShareType
// - Value, FunctionInfo
// - Error, Result
```

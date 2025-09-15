# What is Multi-Party Computation?

Multi-Party Computation (MPC) is a cryptographic technique that enables multiple parties to jointly compute a function over their inputs while keeping those inputs private. Think of it as a way for parties to collaborate on calculations without revealing their sensitive data to each other.

## The Core Problem

Imagine three companies want to find out which one pays the highest average salary without revealing their actual salary data to competitors. Traditionally, they would need to:

1. Trust a third party with their sensitive data, or
2. Reveal their data to each other directly

Both options have serious privacy and competitive disadvantages. MPC provides a third option: compute the answer together without anyone learning anyone else's private data.

## How MPC Works

### The Basic Concept

MPC protocols work by:

1. **Secret Sharing**: Each party's private input is split into multiple "shares" using cryptographic techniques
2. **Distributed Computation**: The computation is performed on these shares across multiple nodes
3. **Result Reconstruction**: The final result is reconstructed from the output shares

Throughout this process, no single party (including the computing nodes) ever sees the raw private data.

### A Simple Example

Consider two parties, Alice and Bob, who want to compute `(Alice's number + Bob's number) > 100` without revealing their numbers:

```
Alice has: 75 (secret)
Bob has: 30 (secret)

1. Secret Sharing:
   Alice's 75 → shares: [23, 17, 35]
   Bob's 30 → shares: [8, 12, 10]

2. Distributed Computation:
   Node 1: 23 + 8 = 31
   Node 2: 17 + 12 = 29
   Node 3: 35 + 10 = 45

   Each node computes: share > threshold_share

3. Result Reconstruction:
   Combine results → 105 > 100 = true
```

Neither Alice nor Bob learns the other's number, but they both learn that their sum exceeds 100.

## Types of MPC

### By Security Model

**Semi-Honest (Honest-but-Curious)**
- Parties follow the protocol correctly but try to learn extra information
- More efficient but assumes participants won't actively cheat
- Suitable for many real-world scenarios where reputation matters

**Malicious**
- Parties may deviate from the protocol arbitrarily
- Stronger security guarantees but higher computational cost
- Required when participants cannot be trusted to follow rules

### By Network Assumptions

**Honest Majority**
- Assumes more than half of participants are honest
- Generally more efficient
- Used by protocols like Stoffel's HoneyBadger MPC

**Dishonest Majority**
- Works even if most participants are malicious
- Higher computational and communication overhead
- Typically used in two-party scenarios

## Real-World Applications

### Financial Services

**Private Credit Scoring**
```
Multiple banks → Collaborative credit risk assessment → Individual scores
(without sharing customer data)
```

**Market Data Analysis**
```
Trading firms → Joint market analysis → Insights
(without revealing trading strategies)
```

### Healthcare

**Medical Research**
```
Hospitals → Disease pattern analysis → Research findings
(without sharing patient records)
```

**Drug Discovery**
```
Pharmaceutical companies → Compound effectiveness → New drugs
(without sharing proprietary research)
```

### Government & Compliance

**Tax Fraud Detection**
```
Tax agencies → Cross-border fraud detection → Investigation leads
(without sharing taxpayer information)
```

**Supply Chain Verification**
```
Companies → Ethical sourcing verification → Compliance reports
(without revealing supplier details)
```

## MPC vs Other Privacy Technologies

| Technology | Privacy Level | Performance | Use Cases |
|------------|---------------|-------------|-----------|
| **MPC** | High - inputs remain secret | Moderate | Multi-party computation |
| **Homomorphic Encryption** | High - single party holds data | Low | Outsourced computation |
| **Differential Privacy** | Medium - statistical privacy | High | Data analysis/sharing |
| **Secure Enclaves** | High - hardware-based | High | Trusted execution |

## Challenges and Limitations

### Performance Considerations

**Computational Overhead**
- MPC operations are significantly slower than plain computation
- Cryptographic operations add substantial cost
- Trade-off between security and performance

**Communication Complexity**
- Multiple rounds of communication between parties
- Network latency affects overall computation time
- Bandwidth requirements can be substantial

### Practical Constraints

**Setup Requirements**
- Coordinating multiple parties can be complex
- Trust assumptions about protocol participants
- Key management and secure channels

**Programming Complexity**
- Traditional programming models don't directly apply
- Need specialized tools and languages
- Debugging and testing require new approaches

## The Promise of MPC

Despite these challenges, MPC offers unprecedented opportunities:

### Enabling New Business Models

**Data Collaboration Without Exposure**
- Competitors can collaborate on common problems
- Data monetization without data sharing
- Cross-organizational analytics

**Regulatory Compliance**
- GDPR-compliant data analysis
- Financial privacy regulations
- Healthcare data protection

### Technical Advantages

**Distributed Trust**
- No single point of failure
- Reduced trust requirements
- Cryptographic security guarantees

**Selective Disclosure**
- Compute only what's needed
- Reveal only specific results
- Fine-grained privacy control

## MPC in Practice

Modern MPC is becoming practical for real applications:

**Performance Improvements**
- Specialized protocols for specific use cases
- Hardware acceleration (GPUs, specialized chips)
- Optimized implementations

**Developer Tools**
- High-level programming languages
- Automated optimization
- Debugging and testing frameworks

**Deployment Infrastructure**
- Cloud-based MPC services
- Standardized protocols
- Integration with existing systems

This is where Stoffel comes in - providing a complete framework that makes MPC accessible to developers without requiring deep cryptographic expertise.

## Next Steps

To understand how Stoffel addresses these challenges and makes MPC practical for developers, see:
- **[Why Stoffel?](./why-stoffel.md)** - How Stoffel solves MPC development challenges
- **[Ecosystem Overview](./ecosystem.md)** - Complete overview of Stoffel's components

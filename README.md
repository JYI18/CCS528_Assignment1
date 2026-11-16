# CCS528_Assignment1
# TASK 1

Task 1 demonstrates the implementation of Shor's Algorithm for integer factorization using Python and Qiskit. The task is developed in three stages. `shor.py` and `shor_quantum.py` perform preliminary testing of classical factorization and basic quantum circuit simulation, while `quantum_circuit.py` implements quantum period finding and classical factor extraction.

**Parameters:**
- Target composite integer: `N = 15`
- Selected base: `a = 2`

## 1. `shor.py`

Demonstrates the classical calculations involved in Shor's Algorithm.

- GCD Check
- Modular Exponentiation
- Period Finding
- Factor Extraction

## 2. `shor_quantum.py`

Performs basic quantum circuit testing using Qiskit.

- Creates a one-qubit circuit and applies a Hadamard gate.
- Measures the qubit using the Qiskit Aer simulator.
- Calculates measurement counts and probabilities.
- Displays a measurement histogram.
- Records circuit depth, gate count and execution time.

## 3. `quantum_circuit.py`

Implements the main quantum period-finding process and classical factor extraction.

## REQUIREMENTS

- Python 3.15.2
- Qiskit
- Qiskit Aer
- Matplotlib

## HOW TO RUN

Run the Python files separately in the following order:

**Step 1: Classical pre-testing**
```bash
python shor.py
```

**Step 2: Preliminary quantum simulation**
```bash
python shor_quantum.py
```

**Step 3: Quantum circuit implementation**
```bash
python quantum_circuit.py
```

## EXPECTED RESULTS

For `N = 15` and `a = 2`, the expected results are:

- Estimated period: `r = 4`
- Factor 1: `3`
- Factor 2: `5`

Quantum measurement results may vary between simulation runs due to the probabilistic nature of quantum measurement.

## CONCLUSION

Task 1 demonstrates Shor's Algorithm through classical calculations, preliminary quantum simulation and the main quantum circuit implementation. It combines quantum period finding with classical post-processing to factor the composite integer 15 into 3 and 5.

---

# TASK 3

Task 3 demonstrates the use of ML-DSA-44 (Module-Lattice-Based Digital Signature Algorithm) for digital signature generation, message authentication and integrity verification using Python.

Two experiments are conducted to evaluate signature verification under different conditions. `experiment_a.py` tests successful verification of an original signed message, while `experiment_b.py` tests the detection of an unauthorised message modification.

Both experiments simulate communication between Alice and Bob, with Eve introduced as an attacker in Experiment B.

## 1. `experiment_a.py`

Demonstrates the digital signature process using an unchanged message.

1. Generates an ML-DSA-44 public-private key pair for Alice.
2. Creates and signs the original message using Alice's private key.
3. Allows Bob to verify the signature using Alice's public key.
4. Records key sizes, signature size and execution times.

**Expected Result:**

Signature VALID. Bob accepts the message.

## 2. `experiment_b.py`

Examines the ability of ML-DSA-44 to detect message modifications.

1. Generates an ML-DSA-44 public-private key pair.
2. Creates and signs the original message.
3. Simulates Eve modifying the meeting time from 3 PM to 9 PM without changing the original signature.
4. Allows Bob to verify the modified message using Alice's public key and original signature.
5. Records key sizes, signature size and execution times.

**Expected Result:**

Signature INVALID. Tampering is detected, and Bob rejects the message.

## REQUIREMENTS

- Python 3.15.2
- Cryptography library with ML-DSA support

## HOW TO RUN

Run the Python files separately in the following order:

**Step 1: Original message verification**
```bash
python experiment_a.py
```

**Step 2: Tampered message verification**
```bash
python experiment_b.py
```

## CONCLUSION

Task 3 demonstrates how ML-DSA-44 provides message authentication and integrity through digital signatures. Experiment A confirms successful verification of an original message, while Experiment B demonstrates the detection of unauthorised message modifications.

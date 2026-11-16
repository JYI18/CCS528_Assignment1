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
# TASK 2

Task 2 demonstrates the use of ML-KEM-768 (Module-Lattice-Based Key Encapsulation Mechanism) together with AES-256 symmetric encryption for secure key establishment and encrypted communication using Python.

The experiment simulates secure communication between Alice and Bob. ML-KEM-768 is used to establish a shared secret, while HKDF-SHA256 derives a common AES-256 session key. AES-GCM is then used to encrypt and decrypt messages securely.

The experiment also measures key generation, encapsulation and decapsulation performance over multiple iterations.

## 1. `mlkem_aes.py`

Demonstrates quantum-safe key establishment and encrypted communication.

1. Bob generates an ML-KEM-768 public-private key pair.
2. Alice performs encapsulation using Bob's public key to establish a shared secret.
3. Bob performs decapsulation to recover the shared secret.
4. Records key-generation, encapsulation, decapsulation execution times, and key sizes.
5. Alice and Bob derive a shared AES-256 key using HKDF-SHA256.
6. Alice encrypts a message using AES-GCM.
7. Bob decrypts the message and verifies that it matches Alice's original message.

**Expected Result:**

Shared secret successfully established. AES key successfully derived. Message encryption and decryption successful.

## PERFORMANCE MEASUREMENTS

The measurements are calculated using 100 iterations to obtain average performance results.

The program records the following measurements:
1. Average key-generation time
2. Average encapsulation time
3. Average decapsulation time
4. Public-key size
5. Private-key size
6. Ciphertext size

## REQUIREMENTS

- Python 3.x
- liboqs-python
- cryptography
- tabulate

## HOW TO RUN

Run the Python file:

```bash
python mlkem_aes.py
```

## CONCLUSION

Task 2 demonstrates how ML-KEM-768 can securely establish a shared secret between communicating parties in a quantum-safe environment. The derived secret is successfully converted into an AES-256 session key using HKDF-SHA256, enabling secure message encryption and decryption through AES-GCM. The performance and key size measurements are recorded in this experiment.

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

---
# TASK 4

Task 4 compares selected classical cryptographic mechanisms with post-quantum cryptographic mechanisms in terms of performance, key sizes, signature sizes and communication overhead.

Two categories of cryptographic operations are evaluated:

1. Key establishment:
- RSA-OAEP-3072
- ML-KEM-768

2. Digital signatures:
- RSA-PSS-3072
- ML-DSA-65

The experiments measure key generation, encryption/encapsulation, decryption/decapsulation, signing, verification, communication overhead, and total execution time.

All experiments are executed automatically through a single main program, which collects the results, stores them in a CSV file and generates performance comparison graphs.

## 1. `crypto_comparison_main.py`

Main controller program.

1. Executes all four experiments.
2. Records performance measurements.
3. Saves the results into a CSV file.
4. Generates comparison graphs for key-generation time and total execution time.

**Expected Result:**

All four experiments should complete successfully. 
The program should generate:

- crypto_comparison_results.csv
- key_generation_comparison.png
- total_execution_comparison.png

## 2. `rsa_oaep_experiment.py`

Evaluates RSA-OAEP-3072 for classical key establishment.

1. Bob generates an RSA-3072 public-private key pair.
2. Bob shares his public key with Alice.
3. Alice generates a random AES session key.
4. Alice encrypts the AES key using Bob's RSA public key and sends the ciphertext to Bob.
5. Bob decrypts the ciphertext using his RSA private key to recover the AES key.
6. The recovered AES key is compared with Alice's original AES key to verify successful key establishment.
7. Performance, key size and communication overhead measurements are recorded.

**Expected Result:**

AES session key successfully encrypted and decrypted. Alice and Bob obtain the same AES key. Verification successful.

## 3. `ml_kem_experiment.py`

Evaluates ML-KEM-768 for post-quantum key establishment.

1. Bob generates an ML-KEM-768 public-private key pair.
2. Bob shares his public key with Alice.
3. Alice performs encapsulation using Bob's public key to generate a ciphertext and shared secret.
4. Alice sends the ciphertext to Bob.
5. Bob performs decapsulation using his private key to recover the shared secret.
6. Alice's and Bob's shared secrets are compared to verify successful key establishment.
7. Performance, key size and communication overhead measurements are recorded.

**Expected Result:**

Shared secret successfully established. Alice and Bob obtain the same shared secret. Verification successful.

## 4. `rsa_pss_experiment.py`

Evaluates RSA-PSS-3072 for classical digital signatures.

1. Alice generates an RSA-3072 public-private key pair.
2. Alice creates and digitally signs a message using her RSA private key.
3. Alice sends the signed message and signature to Bob.
4. Bob verifies the signature using Alice's RSA public key.
5. Performance, signature size and communication overhead measurements are recorded.

**Expected Result:**

Digital signature generated successfully. Signature verification successful.

## 5. `ml_dsa_experiment.py`

Evaluates ML-DSA-65 for post-quantum digital signatures.

1. Alice generates an ML-DSA-65 public-private key pair.
2. Alice creates and digitally signs a message using her ML-DSA private key.
3. Alice sends the signed message and signature to Bob.
4. Bob verifies the signature using Alice's ML-DSA public key.
5. Performance, signature size and communication overhead measurements are recorded.

**Expected Result:**

Digital signature generated successfully. Signature verification successful.

## PERFORMANCE MEASUREMENTS

The program records the following measurements:

1. Key generation time
2. Encryption or encapsulation time
3. Decryption or decapsulation time
4. Signing time
5. Verification time
6. Total execution time
7. Standard deviation
8. Public key size
9. Private key size
10. Ciphertext size
11. Signature size
12. Communication overhead

## REQUIREMENTS

- Python 3.x
- liboqs-python
- cryptography
- pandas
- matplotlib

## HOW TO RUN

Run the Python file:

```bash
python crypto_comparison_main.py
```

## CONCLUSION

Task 4 compares classical and post-quantum cryptographic mechanisms for key establishment and digital signatures. The experiments record performance, key size, signature size and communication overhead measurements to compare classical cryptography and post-quantum cryptography.

---
# TASK 5

Task 5 demonstrates the application of ML-DSA-44 (Module-Lattice-Based Digital Signature Algorithm) in a quantum-safe smart door lock system.

The prototype simulates remote access control between a smartphone application and a smart door lock. ML-DSA-44 is used to provide command authentication and message integrity, while PIN authentication provides an additional access-control mechanism for unlock operations.

The prototype also includes a man-in-the-middle (MITM) attack simulation to demonstrate the ability of ML-DSA-44 to detect command tampering.

## 1. `smart_lock.py`

Demonstrates a quantum-safe smart door lock using ML-DSA-44 digital signatures.

1. The smartphone application generates an ML-DSA-44 public-private key pair.
2. The user selects either a LOCK or UNLOCK operation through the smartphone application.
3. The smartphone application requires PIN authentication before an UNLOCK command can be processed.
4. The smartphone application digitally signs LOCK and UNLOCK commands using the ML-DSA private key.
5. The smart door lock receives the command and verifies the digital signature using the corresponding public key.
6. The smart door lock executes the command only if signature verification is successful.
7. An attacker modifies a signed command during the MITM attack simulation.
8. The smart door lock detects the modified command and rejects it because signature verification fails.

**Expected Result:**

LOCK and UNLOCK commands successfully authenticated. Modified commands are rejected. Verification successful.

## REQUIREMENTS

- Python 3.x
- Cryptography library with ML-DSA support

## HOW TO RUN

Run the Python file:

```bash
python smart_lock.py
```

## CONCLUSION

Task 5 demonstrates how ML-DSA-44 can be applied within a smart home environment to provide quantum-safe authentication and message integrity. The prototype successfully verifies authentic commands and rejects tampered commands, demonstrating the potential of post-quantum cryptography for securing future access control systems.

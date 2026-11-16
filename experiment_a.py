
import time

from cryptography.hazmat.primitives.asymmetric.mldsa import (
    MLDSA44PrivateKey
)
from cryptography.exceptions import InvalidSignature


print("=== Experiment A: Original Message ===")
print("Algorithm: ML-DSA-44")

# Alice generates public and private keys
start = time.perf_counter()

private_key = MLDSA44PrivateKey.generate()
public_key = private_key.public_key()

keygen_time = time.perf_counter() - start

print("\n=== Key Generation ===")
print("Alice generates her key pair.")

# Alice prepares and signs her message
message = b"Hi Bob, let's meet at 3 PM."

print("\n=== Original Message ===")
print("Alice:", message.decode())

start = time.perf_counter()

signature = private_key.sign(message)

signing_time = time.perf_counter() - start

print("Alice signs the message using her private key.")

# 3. Bob verifies Alice's signature
print("\n=== Signature Verification ===")

start = time.perf_counter()

try:
    public_key.verify(signature, message)
    valid = True

except InvalidSignature:
    valid = False

verification_time = time.perf_counter() - start

if valid:
    print("Bob: Signature VALID.")
    print("Bob: Message accepted.")
else:
    print("Bob: Signature INVALID.")
    print("Bob: Message rejected.")

public_key_size = len(public_key.public_bytes_raw())
private_seed_size = len(private_key.private_bytes_raw())
signature_size = len(signature)

print("\n=== Experimental Measurements ===")
print("Public key size:", public_key_size, "bytes")
print("Private key seed size:", private_seed_size, "bytes")
print("Signature size:", signature_size, "bytes")
print(f"Key generation time: {keygen_time:.6f} seconds")
print(f"Signing time: {signing_time:.6f} seconds")
print(f"Verification time: {verification_time:.6f} seconds")

print("\n=== Final Result ===")
print("Experiment A:", "PASS" if valid else "FAIL")

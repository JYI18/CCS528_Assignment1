
import time

from cryptography.hazmat.primitives.asymmetric.mldsa import (
    MLDSA44PrivateKey
)
from cryptography.exceptions import InvalidSignature

print("=== Experiment B: Tampered Message ===")
print("Algorithm: ML-DSA-44")
# Alice generates public and private keys
start = time.perf_counter()
private_key = MLDSA44PrivateKey.generate()
public_key = private_key.public_key()
keygen_time = time.perf_counter() - start

print("\n=== Key Generation ===")
print("Alice generates her key pair.")
# Alice signs the original message
original_message = b"Hi Bob, let's meet at 3 PM."

print("\n=== Original Message ===")
print("Alice:", original_message.decode())

start = time.perf_counter()

signature = private_key.sign(original_message)

signing_time = time.perf_counter() - start

print("Alice signs the original message.")

# Eve modifies the message
tampered_message = b"Hi Bob, let's meet at 9 PM."

print("\n=== Message Tampering ===")
print("Eve intercepts Alice's message.")
print("Eve changes 3 PM to 9 PM.")

print("Modified message:", tampered_message.decode())

# Bob verifies the modified message
print("\n=== Signature Verification ===")
print("Bob uses Alice's original public key.")
print("Bob checks the ORIGINAL signature.")

start = time.perf_counter()

try:
    public_key.verify(signature, tampered_message)
    valid = True

except InvalidSignature:
    valid = False

verification_time = time.perf_counter() - start

if valid:
    print("Bob: Signature VALID.")
    print("WARNING: Tampered message accepted!")
else:
    print("Bob: Signature INVALID.")
    print("Bob: Tampering detected!")
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
print("Experiment B:", "PASS" if not valid else "FAIL")

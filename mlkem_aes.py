import oqs
import time
import os
import statistics

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from tabulate import tabulate

ALGORITHM = "ML-KEM-768"
NUM_ITERATIONS = 100

keygen_times = []
encap_times = []
decap_times = []


for i in range(NUM_ITERATIONS):

    with oqs.KeyEncapsulation(ALGORITHM) as bob:

        # Generate Bob public and private key
        start_time = time.perf_counter()
        bob_public_key = bob.generate_keypair()
        keygen_times.append(time.perf_counter()-start_time)
        
        bob_private_key = bob.export_secret_key()
        
        # Encapsulation
        with oqs.KeyEncapsulation(ALGORITHM) as alice:
            start_time = time.perf_counter()
            ciphertext, alice_shared_secret = alice.encap_secret(bob_public_key)

            encap_times.append(time.perf_counter()-start_time)

        # Decapsulation
        start_time = time.perf_counter()
        bob_shared_secret = bob.decap_secret(ciphertext)
        
        decap_times.append(time.perf_counter()-start_time)

        # Verification
        if alice_shared_secret != bob_shared_secret:
            print("Verification: Failed")
            break      
else:
    # ML-KEM successful verification
    print("\n\n===== ML-KEM =====")
    print("Verification: Success; Alice and Bob obtained the same shared secret")
    print("\nKey generation: Success")
    print("Encapsulation: Success")
    print("Decapsulation: Success")

    # Calculate average times
    avg_keygen = statistics.mean(keygen_times)*1000
    avg_encap = statistics.mean(encap_times)*1000
    avg_decap = statistics.mean(decap_times)*1000

    # Display measurements
    print("\n============ Average Performance Results ============")

    table_data = [
        ["Key-generation time", f"{avg_keygen} ms"],
        ["Encapsulation time", f"{avg_encap} ms"],
        ["Decapsulation time", f"{avg_decap} ms"],
        ["Public-key size", f"{len(bob_public_key)} bytes"],
        ["Private-key size",f"{len(bob_private_key)} bytes"],
        ["Ciphertext size", f"{len(ciphertext)} bytes"]
    ]
    headers = ["Selected Measurements", "Values"]

    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("\nNumber of iterations:", NUM_ITERATIONS)

    print("\n===== AES Symmetric Encryption =====")

    # HKDF-SHA256: AES-256 Key Derivation
    salt = os.urandom(16)
    
    # Alice
    alice_hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"ML-KEM-768 AES session"
        )            
    
    alice_aes_key = alice_hkdf.derive(alice_shared_secret)
    
    # Bob
    bob_hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"ML-KEM-768 AES session"
    )

    bob_aes_key = bob_hkdf.derive(bob_shared_secret)

    # Verify AES key
    if alice_aes_key == bob_aes_key:
        print("AES key derivation: Success; Alice and Bob have the same AES key")

        # Alice encrypt message
        alice_message = b"Hello Bob, this is an encrypted message"
        nonce = os.urandom(12)
        alice_aes = AESGCM(alice_aes_key)

        encrypted_aes = alice_aes.encrypt(nonce, alice_message, None)

        print("\nAES Encryption: Success")
        print("Encrypted message:", encrypted_aes.hex())

        # Bob decrypt message
        bob_aes = AESGCM(bob_aes_key)

        decrypted_aes = bob_aes.decrypt(nonce, encrypted_aes, None)

        print("\nAES Decryption: Success")
        print("Bob's decrypted message:", decrypted_aes.decode())

        # Verify original and decrpyted message
        if alice_message == decrypted_aes:
            print("\nMessage verification: Success")
        else:
            print("\nMessage verification: Failed")

    else:
        print("AES key verivation: Failed")

# ML-KEM verification failed
if len(keygen_times) != NUM_ITERATIONS:
    print("\nExperiment stopped because shared secret verification failed.")

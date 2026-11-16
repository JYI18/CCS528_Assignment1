# Classical RSA-OAEP
# RSA-OAEP uses public-key encryption to transport an AES key

def run_experiment():
    import time
    import os
    import statistics

    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes, serialization

    NUM_ITERATIONS = 30

    # Initialise measurement lists
    keygen_times = []
    encryption_times = []
    decryption_times = []

    for i in range(NUM_ITERATIONS):

        # Bob generates RSA key pair
        start_time = time.perf_counter()
        bob_private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
        bob_public = bob_private.public_key()
        keygen_times.append(time.perf_counter()-start_time)

        # Export public and private keys
        bob_public_bytes = bob_public.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        bob_private_bytes = bob_private.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())

        # Alice generate a random AES key
        alice_aes_key = os.urandom(32)

        # Alice encrypts AES key using Bob's public key
        encrypt_start = time.perf_counter()

        ciphertext = bob_public.encrypt(
            alice_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encryption_times.append(time.perf_counter()-encrypt_start)

        # Bob decrypts ciphertext using his private key
        decrypt_start = time.perf_counter()

        bob_aes_key = bob_private.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        decryption_times.append(time.perf_counter()-decrypt_start)

        # Verification
        if alice_aes_key != bob_aes_key:
            raise RuntimeError("RSA-OAEP AES key verification failed")

    # Calculate average performance
    avg_keygen = statistics.mean(keygen_times)*1000
    avg_encryption = statistics.mean(encryption_times)*1000
    avg_decryption = statistics.mean(decryption_times)*1000
    avg_total_execution = avg_encryption+avg_decryption

    total_execution_times = [
        (enc+dec)*1000
        for enc, dec in zip(encryption_times, decryption_times)
        ]

    std_total_execution = statistics.stdev(total_execution_times)

    # Communication overhead
    communication_overhead = (len(bob_public_bytes) + len(ciphertext))

    # Verification success
    print("\nRRSA-OAEP verification: SUCCESS")
    print("Number of iterations completed:", NUM_ITERATIONS)

    rsa_oaep_results = {
        "Mechanism": "RSA-OAEP",
        "Key-generation time (ms)": avg_keygen,
        "Encryption/Encapsulation time (ms)": avg_encryption,
        "Decryption/Decapsulation time (ms)": avg_decryption,
        "Total execution time (ms)": avg_total_execution,
        "Standard deviation (ms)": std_total_execution,
        "Public key size (bytes)": len(bob_public_bytes),
        "Private key size (bytes)": len(bob_private_bytes),
        "Ciphertext size (bytes)": len(ciphertext),
        "Communication overhead (bytes)": communication_overhead
    }

    return rsa_oaep_results
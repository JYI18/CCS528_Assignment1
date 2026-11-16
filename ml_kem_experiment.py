# ML-KEM-768 uses Key Encapsulation Mechanism(KEM)

def run_experiment():

    import time
    import oqs
    import statistics

    ALGORITHM = "ML-KEM-768"
    NUM_ITERATIONS = 30

    # Initialise measurement lists
    keygen_times = []
    encapsulation_times = []
    decapsulation_times = []

    for i in range(NUM_ITERATIONS):
        with oqs.KeyEncapsulation(ALGORITHM) as bob:

            # Bob generate public and private key
            start_time = time.perf_counter()
            bob_public_key = bob.generate_keypair()
            keygen_times.append(time.perf_counter()-start_time)
            bob_private_key = bob.export_secret_key()

            # Alice encapsulates shared secret
            with oqs.KeyEncapsulation(ALGORITHM) as alice:
                start_time = time.perf_counter()
                ciphertext, alice_shared_secret = alice.encap_secret(bob_public_key)
                encapsulation_times.append(time.perf_counter()-start_time)

            # Bob decapsulates shared secret
            start_time = time.perf_counter()
            bob_shared_secret = bob.decap_secret(ciphertext)
            decapsulation_times.append(time.perf_counter()-start_time)

            # Verification
            if alice_shared_secret != bob_shared_secret:
                raise RuntimeError("ML-KEM verification failed")

    # Calculate average performance
    avg_keygen = statistics.mean(keygen_times)*1000
    avg_encapsulation = statistics.mean(encapsulation_times)*1000
    avg_decapsulation = statistics.mean(decapsulation_times)*1000
    avg_total_execution = avg_encapsulation+avg_decapsulation

    total_execution_times = [
        (enc+dec)*1000
        for enc, dec in zip(encapsulation_times, decapsulation_times)
    ]

    std_total_execution = statistics.stdev(total_execution_times)

    # Communication overhead
    communication_overhead = (len(bob_public_key)+len(ciphertext))

    # Verification success
    print("\nML-KEM verification: SUCCESS")
    print("Number of iterations completed:", NUM_ITERATIONS)

    ml_kem_results = {
            "Mechanism": "ML-KEM",
            "Key-generation time (ms)": avg_keygen,
            "Encryption/Encapsulation time (ms)": avg_encapsulation,
            "Decryption/Decapsulation time (ms)": avg_decapsulation,
            "Total execution time (ms)": avg_total_execution,
            "Standard deviation (ms)": std_total_execution,
            "Public key size (bytes)": len(bob_public_key),
            "Private key size (bytes)": len(bob_private_key),
            "Ciphertext size (bytes)": len(ciphertext),
            "Communication overhead (bytes)": communication_overhead
        }
    
    return ml_kem_results
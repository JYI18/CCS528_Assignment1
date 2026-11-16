# ML-DSA-65

def run_experiment():

    import time
    import statistics
    import oqs
    from cryptography.exceptions import InvalidSignature

    ALGORITHM = "ML-DSA-65"
    NUM_ITERATIONS = 30

    # Initialise measurement lists
    keygen_times = []
    signing_times = []
    verification_times = []

    message = b"UNLOCK DIGITAL LOCK"

    for i in range(NUM_ITERATIONS):
        with oqs.Signature(ALGORITHM) as alice:

            # Alice generate public and private key
            start_time = time.perf_counter()
            alice_public_key = alice.generate_keypair()
            keygen_times.append(time.perf_counter()-start_time)
            alice_private_key = alice.export_secret_key()

            # Alice sign message
            sign_start = time.perf_counter()
            alice_signature = alice.sign(message)
            signing_times.append(time.perf_counter()-sign_start)

        # Bob verify signature
        with oqs.Signature(ALGORITHM) as bob:
            verify_start = time.perf_counter()
            result = bob.verify(message, alice_signature, alice_public_key)
            verification_times.append(time.perf_counter()-verify_start)

            if not result:
                raise RuntimeError("ML-DSA signature verification failed")

    # Calculate average performance
    avg_keygen = statistics.mean(keygen_times)*1000
    avg_signing = statistics.mean(signing_times)*1000
    avg_verification = statistics.mean(verification_times)*1000
    avg_total_execution = avg_signing+avg_verification

    total_execution_times = [
        (sign+verify) * 1000
        for sign, verify in zip(signing_times, verification_times)
    ]

    std_total_execution = statistics.stdev(total_execution_times)

    # Communication overhead
    communication_overhead = (len(alice_public_key)+len(message)+len(alice_signature))

    # Verification success
    print("\nML-DSA verification: SUCCESS")
    print("Number of iterations completed:", NUM_ITERATIONS)

    ml_dsa_results = {
        "Mechanism": "ML-DSA",
        "Key-generation time (ms)": avg_keygen,
        "Signing time (ms)": avg_signing,
        "Verification time (ms)": avg_verification,
        "Total execution time (ms)": avg_total_execution,
        "Standard deviation (ms)": std_total_execution,
        "Public key size (bytes)": len(alice_public_key),
        "Private key size (bytes)": len(alice_private_key),
        "Signature size (bytes)": len(alice_signature),
        "Communication overhead (bytes)": communication_overhead
    }

    return ml_dsa_results
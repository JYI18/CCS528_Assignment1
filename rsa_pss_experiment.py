# Classical RSA-PSS-3072
# RSA-PSS is used for digital signatures

def run_experiment():
    import time
    import statistics

    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.exceptions import InvalidSignature

    NUM_ITERATIONS = 30
    
    # Initialise measurement lists
    keygen_times = []
    signing_times = []
    verification_times = []

    message = b"UNLOCK DIGITAL LOCK"

    for i in range(NUM_ITERATIONS):

        # Alice generates RSA keys
        start_time = time.perf_counter()
        alice_private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
        alice_public = alice_private.public_key()
        keygen_times.append(time.perf_counter()-start_time)

        # Export public and private keys
        alice_public_bytes = alice_public.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
        alice_private_bytes = alice_private.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())

        # Alice signs message
        sign_start = time.perf_counter()

        signature = alice_private.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        signing_times.append(time.perf_counter()-sign_start)

        # Bob verifies signature
        verify_start = time.perf_counter()

        try:
            alice_public.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            verification_times.append(time.perf_counter()-verify_start)

        except InvalidSignature:
            raise RuntimeError("RSA-PSS signature verification failed")

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
    communication_overhead = (len(alice_public_bytes)+len(message)+len(signature))

    # Verification success
    print("\nRSA-PSS verification: SUCCESS")
    print("Number of iterations completed:", NUM_ITERATIONS)

    rsa_pss_results = {
        "Mechanism": "RSA-PSS",
        "Key-generation time (ms)": avg_keygen,
        "Signing time (ms)": avg_signing,
        "Verification time (ms)": avg_verification,
        "Total execution time (ms)": avg_total_execution,
        "Standard deviation (ms)": std_total_execution,
        "Public key size (bytes)": len(alice_public_bytes),
        "Private key size (bytes)": len(alice_private_bytes),
        "Signature size (bytes)": len(signature),
        "Communication overhead (bytes)": communication_overhead
    }

    return rsa_pss_results
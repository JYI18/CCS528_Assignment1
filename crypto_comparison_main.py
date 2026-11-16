import pandas as pd
import matplotlib.pyplot as plt
import os

from rsa_oaep_experiment import run_experiment as run_rsa
from ml_kem_experiment import run_experiment as run_mlkem
from rsa_pss_experiment import run_experiment as run_rsa_signature
from ml_dsa_experiment import run_experiment as run_mldsa

# Run all four experiments
results = []

print("===== TASK 4: CRYPTOGRAPHIC COMPARISON =====")

print("\n1. Running RSA-OAEP...")
results.append(run_rsa())

print("\n2. Running ML-KEM...")
results.append(run_mlkem())

print("\n3. Running RSA Signature...")
results.append(run_rsa_signature())

print("\n4. Running ML-DSA...")
results.append(run_mldsa())


# Save results to csv
df = pd.DataFrame(results)

output_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "crypto_comparison_results.csv"
)

df.to_csv(output_path, index=False)

print("\n===== EXPERIMENT COMPLETED =====")
print("\nAll results saved successfully! File location:", output_path)

# Read experimental results
df = pd.read_csv("crypto_comparison_results.csv")

# Graph 1: Key-generation time
plt.figure(figsize=(9, 5))

generation_bar = plt.bar(
    df["Mechanism"],
    df["Key-generation time (ms)"],
    color="skyblue"
)

plt.bar_label(generation_bar, fmt="%.3f", padding=3, fontsize = 8)
plt.yscale("log")

plt.title("Key Generation Time Comparison")
plt.xlabel("Cryptographic Mechanism")
plt.ylabel("Time (ms)")
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig("key_generation_comparison.png", dpi=300)
plt.close()


# Graph 2: Total execution eime
plt.figure(figsize=(9, 5))

execution_bar = plt.bar(
    df["Mechanism"],
    df["Total execution time (ms)"],
    color="orange"
)

plt.bar_label(execution_bar, fmt="%.3f", padding=3,fontsize = 8)

plt.title("Total Execution Time Comparison")
plt.xlabel("Cryptographic Mechanism")
plt.ylabel("Time (ms)")
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig("total_execution_comparison.png", dpi=300)
plt.close()

print("Performance graphs saved successfully!")

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import time

# Create 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply Hadamard gate to create superposition
qc.h(0)

# Measure the qubit
qc.measure(0, 0)

print("\n=== Preliminary Quantum Circuit ===")
print(qc.draw(output="text"))

# Quantum Simulation
simulator = AerSimulator()

shots = 1000

start_time = time.perf_counter()

result = simulator.run(
    qc,
    shots=shots
).result()

execution_time = time.perf_counter() - start_time

counts = result.get_counts()

# Measurement results

print("\n=== Measurement Results ===")

count_0 = counts.get("0", 0)
count_1 = counts.get("1", 0)

prob_0 = count_0 / shots
prob_1 = count_1 / shots

print("State 0:", count_0)
print("State 1:", count_1)

print("\n=== Measurement Probabilities ===")

print(f"P(0) = {prob_0:.4f} ({prob_0 * 100:.2f}%)")
print(f"P(1) = {prob_1:.4f} ({prob_1 * 100:.2f}%)")

# Measurement Histogram

states = ["0", "1"]
frequencies = [count_0, count_1]

fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.bar(
    states,
    frequencies,
    width=0.5
)

ax.set_xlabel("Measured State")
ax.set_ylabel("Frequency")
ax.set_title("Preliminary Quantum Measurement Results")
ax.set_ylim(0, shots * 0.65)

for bar in bars:
    height = bar.get_height()

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 5,
        str(int(height)),
        ha="center",
        va="bottom"
    )

fig.tight_layout()
plt.show()


# Output

print("\n=== Experimental Measurements ===")

print("Number of qubits:", qc.num_qubits)
print("Number of classical bits:", qc.num_clbits)
print("Circuit depth:", qc.depth())
print("Gate count:", qc.count_ops())
print("Number of shots:", shots)

print(f"Simulation execution time: {execution_time:.6f} seconds")

print("\n=== Result Evaluation ===")

print("Expected probability of state 0: 50%")
print("Expected probability of state 1: 50%")

print(f"Observed probability of state 0: {prob_0 * 100:.2f}%")
print(f"Observed probability of state 1: {prob_1 * 100:.2f}%")

print("\nPreliminary quantum simulation completed.")

import math
import time
from fractions import Fraction

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

# N=15
def M2mod15():
    """
    Quantum gate implementing multiplication by 2 mod 15.
    """
    U = QuantumCircuit(4)

    U.swap(2, 3)
    U.swap(1, 2)
    U.swap(0, 1)

    gate = U.to_gate()
    gate.name = "M_2"

    return gate


def M4mod15():
    """
    Quantum gate implementing multiplication by 4 mod 15.
    """
    U = QuantumCircuit(4)

    U.swap(1, 3)
    U.swap(0, 2)

    gate = U.to_gate()
    gate.name = "M_4"

    return gate

# GCD check
N = 15
a = 2

print("\n=== Shor's Algorithm ===")
print("N =", N)
print("a =", a)

gcd_value = math.gcd(a, N)

print("\n=== GCD Check ===")
print("gcd(a, N) =", gcd_value)

if gcd_value > 1:
    print("Factor found directly:", gcd_value)
    print("Other factor:", N // gcd_value)
    raise SystemExit

print("GCD = 1. Proceeding to quantum period finding.")

num_target = 4

num_control = 8

control = QuantumRegister(num_control, "control")
target = QuantumRegister(num_target, "target")
classical = ClassicalRegister(num_control, "measure")

circuit = QuantumCircuit(control, target, classical)

# Target Register
circuit.x(target[0])

# insert control qubits into superposition
for q in control:
    circuit.h(q)

# Controlled modular exponentiation
M2 = M2mod15()
M4 = M4mod15()

circuit.append(
    M2.control(),
    [control[0]] + list(target)
)

circuit.append(
    M4.control(),
    [control[1]] + list(target)
)

# Inverse Quantum Fourier Transform
inverse_qft = QFT(
    num_control,
    inverse=True,
    do_swaps=True
)

circuit.compose(
    inverse_qft,
    qubits=control,
    inplace=True
)

circuit.measure(control, classical)

print("\n=== Quantum Circuit Information ===")

print("Number of qubits:", circuit.num_qubits)
print("Control qubits:", num_control)
print("Target qubits:", num_target)

print("High-level circuit depth:", circuit.depth())
print("High-level gate count:", circuit.count_ops())

print("\nQuantum Circuit:")
print(circuit.draw(output="text", fold=120))


# Quantum Simulation
simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

shots = 1024

start_time = time.perf_counter()

job = simulator.run(
    compiled_circuit,
    shots=shots
)

result = job.result()

execution_time = time.perf_counter() - start_time

counts = result.get_counts()

print("\n=== Experimental Measurements ===")
print("Total qubits:", circuit.num_qubits)
print("Transpiled circuit depth:", compiled_circuit.depth())
print("Transpiled gate count:", compiled_circuit.count_ops())
print("Number of shots:", shots)
print(f"Simulation time: {execution_time:.6f} seconds")

print("\n=== Quantum Measurement Results ===")

for bitstring, count in sorted(
    counts.items(),
    key=lambda item: item[1],
    reverse=True
):
    print(f"{bitstring}: {count}")

print("\n=== Period Estimation ===")

candidate_periods = []

for bitstring, count in sorted(
    counts.items(),
    key=lambda item: item[1],
    reverse=True
):

    decimal = int(bitstring, 2)

    phase = decimal / (2 ** num_control)

    fraction = Fraction(
        decimal,
        2 ** num_control
    ).limit_denominator(N)

    r_guess = fraction.denominator

    print(
        f"{bitstring} -> "
        f"decimal={decimal}, "
        f"phase={phase:.4f}, "
        f"fraction={fraction}, "
        f"candidate r={r_guess}"
    )

    # Check whether the candidate satisfies
    # a^r mod N = 1

    if (
        r_guess > 1
        and pow(a, r_guess, N) == 1
    ):
        candidate_periods.append(r_guess)

if not candidate_periods:
    print("\nNo valid period found.")
    print("Run the experiment again.")
    raise SystemExit

r = min(candidate_periods)

print("\nEstimated valid period r =", r)

# Verify that the estimated period is valid
if pow(a, r, N) != 1:
    print("Period verification failed.")
    raise SystemExit

print(f"Verification: {a}^{r} mod {N} = 1")

print("\n=== Classical Factor Extraction ===")
# A usable period must be even
if r % 2 != 0:
    print("Period is odd. Cannot extract factors.")
    raise SystemExit

half_power = pow(a, r // 2, N)

if half_power == N - 1:
    print("Trivial case: a^(r/2) = -1 mod N.")
    print("Choose another value of a.")
    raise SystemExit

factor1 = math.gcd(half_power - 1, N)
factor2 = math.gcd(half_power + 1, N)

print("Factor 1 =", factor1)
print("Factor 2 =", factor2)

# Verify extracted factors
print("\n=== Final Verification ===")

if (
    1 < factor1 < N
    and 1 < factor2 < N
    and factor1 * factor2 == N
):
    print("Factorisation successful!")
    print(f"{N} = {factor1} x {factor2}")
else:
    print("Factor extraction unsuccessful.")

print("\n=== Final Summary ===")

print("Target integer:", N)
print("Selected base:", a)
print("Estimated period:", r)
print("Extracted factors:", factor1, factor2)
print("Total qubits:", circuit.num_qubits)
print("Shots:", shots)
print(f"Simulation time: {execution_time:.6f} seconds")

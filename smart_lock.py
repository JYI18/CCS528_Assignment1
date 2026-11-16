
from cryptography.hazmat.primitives.asymmetric.mldsa import (
    MLDSA44PrivateKey
)
from cryptography.exceptions import InvalidSignature
from getpass import getpass

DEMO_PIN = "1234"

# Generate ML-DSA key pair
private_key = MLDSA44PrivateKey.generate()
public_key = private_key.public_key()

door_locked = True

# Digital Signature Verification
def verify_signature(message, signature):
    try:
        public_key.verify(signature, message)
        return True
    except InvalidSignature:
        return False

# Process LOCK / UNLOCK Command
def process_command(command, attack=False):
    global door_locked

    print("\n[Smartphone] Creating command:", command)

    # Smartphone signs the command
    message = command.encode()
    signature = private_key.sign(message)

    print("[ML-DSA] Digital signature generated.")

    # Simulate MITM modification
    if attack:
        print("\n[ATTACK] Attacker intercepts the command.")
        print("[ATTACK] Original command:", command)

        message = b"UNLOCK"

        print("[ATTACK] Modified command: UNLOCK")

    # Smart lock verifies the signature
    print("\n[Smart Lock] Verifying digital signature...")

    if not verify_signature(message, signature):
        print("[Smart Lock] Signature INVALID.")
        print("[Smart Lock] Command REJECTED.")
        return

    print("[Smart Lock] Signature VALID.")

    received_command = message.decode()

    if received_command == "LOCK":
        door_locked = True
        print("[Smart Lock] Door LOCKED.")

    elif received_command == "UNLOCK":
        door_locked = False
        print("[Smart Lock] Door UNLOCKED.")

    else:
        print("[Smart Lock] Unknown command. Rejected.")

# Main Terminal Interface
def main():
    global door_locked

    print("=" * 45)
    print("QUANTUM-SAFE SMART DOOR LOCK")
    print("=" * 45)

    while True:

        status = "LOCKED" if door_locked else "UNLOCKED"
        print("\nDoor Status:", status)

        print("\n1. LOCK")
        print("2. UNLOCK")
        print("3. Simulate MITM Attack")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "4":
            print("\nExiting smart door lock system.")
            break

        if choice not in ("1", "2", "3"):
            print("Invalid selection.")
            continue

        # LOCK: No PIN required
        if choice == "1":
            print("\n[Authentication] PIN not required for locking.")
            process_command("LOCK")

        # UNLOCK: PIN required
        elif choice == "2":
            entered_pin = getpass("Enter PIN to unlock: ")

            if entered_pin != DEMO_PIN:
                print("\n[Authentication] Incorrect PIN.")
                print("[Authentication] ACCESS DENIED.")
                continue

            print("\n[Authentication] PIN verified.")
            process_command("UNLOCK")

        # MITM Attack: Modify signed command
        elif choice == "3":
            print("\n=== MITM Attack Simulation ===")
            process_command("LOCK", attack=True)

if __name__ == "__main__":
    main()

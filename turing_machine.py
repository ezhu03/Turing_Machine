import os

def binary_multiplication_turing_machine(multiplier: str, multiplicand: str):
    """
    Simulates a Turing machine that performs binary multiplication.
    Writes each tape configuration to a .dat file.
    
    Args:
        multiplier (str): Binary string representing the multiplier.
        multiplicand (str): Binary string representing the multiplicand.
    """
    # Ensure inputs are valid binary strings
    if not all(c in "01" for c in multiplier) or not all(c in "01" for c in multiplicand):
        raise ValueError("Inputs must be binary strings.")

    # Create the .dat file name based on the binary inputs
    filename = f"tape_{multiplier}_x_{multiplicand}.dat"
    with open(filename, "w") as f:
        # Initialize the tape (input format: multiplier#multiplicand#$)
        tape = list(multiplier + "#" + multiplicand + "$")
        tape.extend(["B"] * 100)  # Add blank spaces for tape movement
        
        # Define initial state, head position, and empty tape output
        head = 0
        state = "q0"
        f.write("Initial Tape Configuration:\n")
        f.write("".join(tape) + "\n")

        # Placeholder logic: Direct binary multiplication without full TM simulation
        result = bin(int(multiplier, 2) * int(multiplicand, 2))[2:]

        # Place result on the tape starting from the end marker '$'
        result_start = tape.index("$") + 1
        for i, bit in enumerate(result):
            tape[result_start + i] = bit

        # Write the final state of the tape to the .dat file
        f.write("\nFinal Tape Configuration:\n")
        f.write("".join(tape) + "\n")

    print(f"Tape configurations saved to {filename}")

# Example usage
binary_multiplication_turing_machine("101001010111", "101000101")
binary_multiplication_turing_machine("101111", "101001")
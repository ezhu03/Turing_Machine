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
        maxsize = len(multiplier) + len(multiplicand)
        bs = "B"*maxsize
        tape = list(bs + multiplier + "*" + multiplicand + bs)
        #tape.extend(["B"] * 20)
        head = maxsize
        state = "start"

        def write_tape():
            f.write(f"State: {state}, Head: {head}, Tape: {''.join(tape)}\n")

        write_tape()
        
        while state != "done":
            symbol = tape[head]
            #print(state, symbol)
            if state == "start":
                if symbol in "01":
                    head -= 1
                    state = "init"
            elif state == "init":
                if symbol == "B":
                    tape[head] = "+"
                    head += 1
                    state = "right"
            elif state == "right":
                if symbol in "01*":
                    head += 1
                elif symbol == "B":
                    head -= 1
                    state = "readB"
            elif state == "readB":
                if symbol == "0":
                    tape[head] = "B"
                    head -= 1
                    state = "doubleL"
                elif symbol == "1":
                    tape[head] = "B"
                    head -= 1
                    state = "addA"
            elif state == "addA":
                if symbol in "01":
                    head -= 1
                elif symbol == "*":
                    head -= 1
                    state = "read"
            elif state == "doubleL":
                if symbol in "01":
                    head -= 1
                elif symbol == "*":
                    tape[head] = "0"
                    head += 1
                    state = "shift"
            elif state == "double":
                if symbol in "01+":
                    head += 1
                elif symbol == "*":
                    tape[head] = "0"
                    head += 1
                    state = "shift"
            elif state == "shift":
                if symbol == "0":
                    tape[head] = "*"
                    head += 1
                    state = "shift0"
                elif symbol == "1":
                    tape[head] = "*"
                    head += 1
                    state = "shift1"
                elif symbol == "B":
                    head -= 1
                    state = "tidy"
            elif state == "shift0":
                if symbol == "0":
                    head += 1
                elif symbol == "1":
                    tape[head] = "0"
                    head += 1
                    state = "shift1"
                elif symbol == "B":
                    tape[head] = "0"
                    head += 1
                    state = "right"
            elif state == "shift1":
                if symbol == "0":
                    tape[head]="1"
                    head += 1
                    state = "shift0"
                elif symbol == "1":
                    head += 1
                elif symbol == "B":
                    tape[head] = "1"
                    head += 1
                    state = "right"
            elif state == "tidy":
                if symbol in "01":
                    tape[head] = "B"
                    head -= 1
                elif symbol == "+":
                    tape[head] = "B"
                    head -= 1
                    state = "done"
            elif state == "read":
                if symbol == "0":
                    tape[head] = "c"
                    head -= 1
                    state = "have0"
                elif symbol == "1":
                    tape[head] = "c"
                    head -= 1
                    state = "have1"
                elif symbol == "+":
                    head -= 1
                    state = "rewrite"
            elif state == "have0":
                if symbol in "01":
                    head -= 1
                elif symbol == "+":
                    head -= 1
                    state = "add0"
            elif state == "have1":
                if symbol in "01":
                    head -= 1
                elif symbol == "+":
                    head -= 1
                    state = "add1"
            elif state == "add0":
                if symbol in "0B":
                    tape[head] = "O"
                    head += 1
                    state = "back0"
                elif symbol == "1":
                    tape[head] = "I"
                    head += 1
                    state = "back0"
                elif symbol in "OI":
                    head -= 1
            elif state == "add1":
                if symbol in "0B":
                    tape[head] = "I"
                    head += 1
                    state = "back1"
                elif symbol == "1":
                    tape[head] = "O"
                    head -= 1
                    state = "carry"
                elif symbol in "OI":
                    head -= 1
            elif state == "carry":
                if symbol in "0B":
                    tape[head] = "1"
                    head += 1
                    state = "back1"
                elif symbol == "1":
                    tape[head] = "0"
                    head -= 1
            elif state == "back0":
                if symbol in "01OI+":
                    head += 1
                elif symbol == "c":
                    tape[head] = "0"
                    head -= 1
                    state = "read"
            elif state == "back1":
                if symbol in "01OI+":
                    head += 1
                elif symbol == "c":
                    tape[head] = "1"
                    head -= 1
                    state = "read"
            elif state == "rewrite":
                if symbol == "O":
                    tape[head] = "0"
                    head -= 1
                elif symbol == "I":
                    tape[head] = "1"
                    head -= 1
                elif symbol in "01":
                    head -= 1
                elif symbol == "B":
                    head += 1
                    state = "double"
            
            write_tape()

    print(f"Tape configurations saved to {filename}")
    return ''.join(tape[:tape.index("B")])


# Example usage
print(binary_multiplication_turing_machine("11", "101"))
print(binary_multiplication_turing_machine("101001010111", "101000101"))
print(binary_multiplication_turing_machine("101111", "101001"))

import os
from itertools import product
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import random

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
    #filename = f"tape_{multiplier}_x_{multiplicand}.dat"
    #with open(filename, "w") as f:
        # Initialize the tape (input format: multiplier#multiplicand#$)
    maxsize = len(multiplier) + len(multiplicand)
    bs = "B"*maxsize
    tape = list(bs + multiplier + "*" + multiplicand + bs)
    #tape.extend(["B"] * 20)
    head = maxsize
    state = "start"

    def write_tape():
        f.write(f"State: {state}, Head: {head}, Tape: {''.join(tape)}\n")

        #write_tape()
    iterations = 0
    while state != "done":
        iterations +=1
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
            
            #write_tape()

    #print(f"Tape configurations saved to {filename}")
    #os.remove(filename)
    #return ''.join(tape[:tape.index("B")])
    return iterations


# Example usage
#print(binary_multiplication_turing_machine("11", "101"))
#print(binary_multiplication_turing_machine("101001010111", "101000101"))
#print(binary_multiplication_turing_machine("101111", "101001"))
def get_iterations(a,b,maxit = 100):

    binary_a = ["".join(bits) for bits in product("01", repeat=a)]
    binary_b = ["".join(bits) for bits in product("01", repeat=b)]
    iters = []
    counter = 0
    if len(binary_a) * len(binary_b) < maxit:
        for numa in binary_a:
            print(numa,"running...")
            for numb in binary_b:
                n = binary_multiplication_turing_machine(numa, numb)
                iters.append(n)
    else:
        for i in range(maxit):
            numa = random.choice(binary_a)
            numb = random.choice(binary_b)
            n = binary_multiplication_turing_machine(numa, numb)
            iters.append(n)
    avg = sum(iters)/len(iters)
    print(min(iters),avg, max(iters))
    # Plot the histogram
    '''plt.figure()
    plt.hist(iters, bins= 20, range = (min(iters), max(iters) + 2),density = True)
    plt.xlabel("Iterations")
    plt.ylabel("Frequency")
    plt.title("Histogram of Iterations for " + str(a) + "x" + str(b) + " Binary Multiplication Turing Machine")  # Ensure discrete ticks
    plt.show()
    plt.savefig("binary_multiplication_iterations" + str(a) + "x" + str(b) +".png")'''
    return avg

'''get_iterations(2,3)
get_iterations(3,2)
get_iterations(3,5)
get_iterations(5,3)
get_iterations(3,12)
get_iterations(12,3)'''
size = 26
values = np.zeros((size,size))
for i in range(size):
    for j in range(size):
        if i>1 and j>1:
            values[i,j] = get_iterations(i,j)
import numpy as np
import matplotlib.pyplot as plt

# Create a figure and axis
plt.figure(figsize=(20, 16))

sns.heatmap(
    values,
    annot=True,          # Show values
    fmt=".0f",           # Format to 2 decimal places (adjust as needed)
    cmap="viridis",
    annot_kws={"size": 6},  # Adjust font size for annotations
    square=True,
    cbar_kws={"shrink": 0.8}  # Adjust colorbar size
)

plt.title("Heatmap of Average Iterations for Binary Multiplication Turing Machine")
plt.show()
plt.savefig("heatmap.png")
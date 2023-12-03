# Given four colors, find correct order

from logic import *
import time

# Record the start time
start_time = time.time()

# Your code block here
colors = ["blue", "red", "green", "yellow"]
symbols = []
knowledge = And()

for i in range(4):
    for color in colors:
        symbols.append(Symbol(f"{color}{i}"))


















# For example, a loop that takes some time
for i in range(1000000):
    pass

# Record the end time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

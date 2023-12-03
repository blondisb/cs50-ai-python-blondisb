from logic import *
import time

# Record the start time
start_time = time.time()

# Your code block here
people = ["Gilderoy", "Pomona", "Minerva", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

symbols = []

knowledge = And()

for person in people:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))

# Each person belongs to a house.
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gryffindor"),
        Symbol(f"{person}Hufflepuff"),
        Symbol(f"{person}Ravenclaw"),
        Symbol(f"{person}Slytherin")
    ))



# Only one house per person.
for person in people:
    for h1 in houses:
        for h2 in houses:
            if h1 != h2:
                knowledge.add(
                    Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}")))
                )
# Only one person per house.
for house in houses:
    for p1 in people:
        for p2 in people:
            if p1 != p2:
                knowledge.add(
                    Implication(Symbol(f"{p1}{house}"), Not(Symbol(f"{p2}{house}")))
                )

knowledge.add(
    Or(Symbol("GilderoyGryffindor"), Symbol("GilderoyRavenclaw"))
)

knowledge.add(
    Not(Symbol("PomonaSlytherin"))
)

knowledge.add(
    Symbol("MinervaGryffindor")
)


aa = 0
for symbol in symbols:
    aa += 1
    # print(aa)
    if model_check(knowledge, symbol):
        print(symbol)









# For example, a loop that takes some time
for i in range(1000000):
    pass

# Record the end time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

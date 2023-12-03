
from logic import *
import time

# Record the start time
start_time = time.time()

# Your code block here
people = ["Gil", "Pom", "Min", "Hor"]
houses = ["Gry", "Huf", "Rav", "Sly"]

symbols = []
knowledge = And()

for person in people:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))

# Each person belong to a house
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gry"),
        Symbol(f"{person}Huf"),
        Symbol(f"{person}Rav"),
        Symbol(f"{person}Sly")
    ))

# Only one house per person
for person in people:
    for h1 in houses:
        for h2 in houses:
            if h1 != h2:
                knowledge.add(
                    Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}")))
                )

# Only one house per person
for house in houses:
    for p1 in people:
        for p2 in people:
            if p1 != p2:
                knowledge.add(
                    Implication(Symbol(f"{p1}{house}"), Not(Symbol(f"{p2}{house}")))
                )

# knowledge.add(Or(symbols[0], symbols[2]))
knowledge.add(Or(Symbol("GilGry"), Symbol("GilRav")))
knowledge.add(Not(Symbol("PomSly")))
knowledge.add(Symbol("MinGry"))


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


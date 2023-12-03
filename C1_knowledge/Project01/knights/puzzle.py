from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

Apair = (AKnight, AKnave)
Bpair = (BKnight, BKnave)
Cpair = (CKnight, CKnave)


""" _____________ PRBOBLEM LOGIC SCTRUCTURE _____________"""
def fn_Xor(pair):
    (P, Q) = pair
    return And(Or(P, Q), Not(And(P, Q)))

def fn_Saids(pair, said):
    (knight, knave) = pair
    return And(Implication(knight, said), Implication(knave, Not(said)))
""" _____________ __________________________ _____________"""

# Puzzle 0
# A says "I am both a knight and a knave."
said = And(AKnight, AKnave)
knowledge0 = And(
    # TODO
    fn_Xor(Apair),
    fn_Saids(Apair, said)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Asaid = And(AKnave, BKnave)
Bsaid = And()
knowledge1 = And(
    # TODO
    fn_Xor(Apair),
    fn_Xor(Bpair),
    fn_Saids(Apair, Asaid),
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Asaid = Or(And(AKnave, BKnave), And(AKnight, BKnight))
Bsaid = Or(And(AKnave, BKnight), And(AKnight, BKnave))
knowledge2 = And(
    # TODO
    fn_Xor(Apair),
    fn_Xor(Bpair),
    fn_Saids(Apair, Asaid),
    fn_Saids(Bpair, Bsaid),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Asaid = Or(AKnight, AKnave)
Bsaid1 = fn_Saids(Apair, AKnave)
Bsaid2 = CKnave
Csaid = AKnight
knowledge3 = And(
    # TODO
    fn_Xor(Apair),
    fn_Xor(Bpair),
    fn_Xor(Cpair),
    fn_Saids(Apair, Asaid),
    fn_Saids(Bpair, Bsaid1),
    fn_Saids(Bpair, Bsaid2),
    fn_Saids(Cpair, Csaid),
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
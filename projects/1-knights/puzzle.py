from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnave, AKnight),
    Not(AKnight),
    AKnave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
# -> A is a Knave, B is a Knight
knowledge1 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Not(And(BKnave, AKnave)),
    Or(Not(AKnave), Not(BKnave)),
    Not(AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# -> A is a Knave, B is a Knight
knowledge2 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(Not(And(AKnave, BKnave)),
    Not(And(AKnight, BKnight))),
    Or(And(AKnave, BKnight),
    And(AKnight, BKnave)),
    Not(AKnight),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# -> A is a Knight, B is a Knave, C is a Knave
knowledge3 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    Or(AKnight, (AKnave)),
    BKnight,
    AKnave,
    CKnave,
    Not(AKnight),
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

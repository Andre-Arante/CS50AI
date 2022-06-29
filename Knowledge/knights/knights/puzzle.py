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
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # If A is Knight and telling the truth, A is both knight and knave
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is knave and lying, A is either not a knight or not a knave
    Implication(AKnave, Or(Not(AKnight), Not(AKnave)))
)
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Knight or Knave, but not both (rule of game)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

   # If A is Knight and telling the truth, then A and B are both Knaves
   Implication(AKnight, And(AKnave, BKnave)),

   # If A is Knave and lying, then A is not a Knave or B is not a Knave
   Implication(AKnave, Or(Not(AKnave), Not(BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Knight or Knave, but not both (rule of game)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is Knight, A and B are the same
    Implication(AKnight, And(AKnight, BKnight)),
    # If A is Knave and lying, A and B are different
    Implication(AKnave, And(AKnave, BKnight)),

    # IF B is Knight, A and B are different
    Implication(BKnight, And(BKnight, AKnave)),
    # If by is Knave and lying, A and B are the same
    Implication(BKnave, And(AKnave, BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Knight or Knave, but not both (rule of game)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A is either knight or knave (true statement so A must be knight)
    Implication(AKnave, And(AKnight, AKnave)),

    # B says A is knave (proven false so B must be knave)
    Implication(BKnight, AKnave),

    # B says C is knave (B is proven knave so C must be knight)
    Or(And(BKnight, CKnave), CKnight),

    # C says A is Knight(already know C is knight and A is knight so everything matches up)
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)

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

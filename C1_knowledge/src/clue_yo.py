import termcolor
import colorama
from logic import *

colorama.init()

mus     = Symbol('Mustard')
plu     = Symbol('ProfPlum')
sca     = Symbol('ScaJohansson')
charachters = [mus, plu, sca]

bal     = Symbol('ballron')
kit     = Symbol('kitchen')
lib     = Symbol('library')
rooms = [bal, kit, lib]

rev     = Symbol('revolver')
kni     = Symbol('knife')
pen     = Symbol('pencil')
weapons = [rev, kni, pen]

symbols = charachters + rooms + weapons

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}: MURDER", "red")
        elif not model_check(knowledge, Not(symbol)):
            termcolor.cprint(f"{symbol}: MAYBE", "yellow")
        else:
            termcolor.cprint(f"{symbol}: CLEAN", "green")

knowledge = And(
    Or(mus, sca, plu),
    Or(bal, kit, lib),
    Or(rev, pen, kni))

knowledge.add(Not(mus))
knowledge.add(Not(rev))
knowledge.add(Not(kit))

# At least one of them, is clean.
knowledge.add(Or(Not(sca), Not(pen), Not(lib)))

knowledge.add(Not(plu))
knowledge.add(Not(bal))


print(knowledge.formula())
check_knowledge(knowledge)
from logic import * 

# 1. If it didn’t rain, Harry visited Hagrid today.
# 2. Harry visited Hagrid or Dumbledore today, but not both.
# 3. Harry visited Dumbledore today.

rain    = Symbol('rain')      # P = It is raining
hag     = Symbol('hagrid')    # Q1 Harry visited hagrid
dumb    = Symbol('dumbledore')# Q2 Harry visited Dumbledore
aa = 'aa'

sentence    = And(rain, hag)
print(type(sentence), sentence.formula())

#--

knowledge   = Implication(Not(rain), hag)
print(type(knowledge), knowledge.formula())

knowledge2   = Or(hag, dumb)
print(type(knowledge2), knowledge2.formula())

knowledge3   = And(knowledge, knowledge2)
print(type(knowledge3), knowledge3.formula())

#--

knowledge   = And(
    Implication(Not(rain), hag),
    Or(hag, dumb),
    Not(And(hag, dumb)),
    dumb
)
print(type(knowledge), knowledge.formula())

#--

print(model_check(knowledge, rain))
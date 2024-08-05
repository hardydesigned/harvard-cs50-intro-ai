from logic import *

rain = Symbol("rain") # It is raining
hagrid = Symbol("hagrid") # Harry visited Hagrid
dumbledore = Symbol("dumbledore") # Harry visited Dumbledore



knowledge = And(
    Implication(Not(rain), hagrid), # If it is not raining, Harry visited Hagrid
    Or(hagrid, dumbledore), # Harry visited Hagrid or Dumbledore
    Not(And(hagrid, dumbledore)), # Harry did not visit both Hagrid and Dumbledore
    dumbledore # Harry visited Dumbledore
)
# (If it is not raining, Harry visited Hagrid) and (Harry visited Hagrid or Dumbledore) and (Harry did not visit both Hagrid and Dumbledore) and (Harry visited Dumbledore)

print(model_check(knowledge, rain))
#print(knowledge.formula()) # ((¬rain) => hagrid) ∧ (hagrid ∨  dumbledore) ∧) ∧ (¬(hagrid ∧ dumbledore)) ∧ ) ∧ (¬(hagrid ∧ dumbledore)) ∧ dumbledore
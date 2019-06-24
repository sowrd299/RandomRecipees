import random
from collections import defaultdict

# how many total units per recipee
total = 1.5

# how many decimals to round to
decimals = 1

# the units of measurement, in both numbers
unit = "Cup"
units = "Cups"

class Ingredient():

    next_id = 0

    def __init__(self, name, mi = 0, ma = total):
        self.name = name 
        self.min = mi
        self.max = ma

        # set up unique ID
        self.id = self.next_id
        Ingredient.next_id += 1

# all the different ingredients to include
ingredients = [
    Ingredient("Silly Circles", 0, 0.4),
    Ingredient("Toasted O's", 0.2),
    Ingredient("Oister Crackers"),
    Ingredient("Gold Fish", 0, 0.4),
    Ingredient("Raisins"),
    Ingredient("Skittles", 0.1, 0.3)
]

def gen_recipee(ingredients, total, decimals):

    class BadGenerationError(Exception):
        pass

    ingr = list(ingredients)

    for _ in range(100):
        total_used = 0 # an accumulator for how much space we have used
        amounts = defaultdict(int)
        try:
            while total_used < total: # keep going until we fill the recipee
                random.shuffle(ingr) # need to do this every time to not favor the begining
                for i in ingr:
                    mi = i.min - amounts[i.id]
                    ma = min(total-total_used, i.max-amounts[i.id])
                    # handle bad cases
                    if mi > ma:
                        raise BadGenerationError
                    # generate the amount
                    amount = random.uniform(mi, ma)
                    # do rounding
                    amount = round(amount, decimals)
                    # store the value
                    amounts[i.id] += amount
                    total_used += amount

            return [(i, amounts[i.id]) for i in ingr]
        except BadGenerationError as e:
            pass

    # the generation failed, possibly due to bad parameters
    return None

if __name__ == "__main__":

    for i in range(40):
        recipee = gen_recipee(ingredients, total, decimals)
        print("Trail Mix Investigation, Sample #"+str(i+1))
        for ingredient, amount in recipee:
            if amount > 0:
                print("{0:.{1}f}".format(amount, decimals), units if amount > 1 else unit, ingredient.name) 

        print("\n\n")

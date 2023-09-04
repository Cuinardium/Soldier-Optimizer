import math
import random
from individual.character import Character
from typing import Callable, Dict, Tuple

CHROMOSOME_LENGTH = 6

# --------------------- Methods --------------------- #

# Selects a random point in the chromosome and a random amount of genes to cross
def __anular(parent1: Character, parent2: Character) -> Tuple[Character, Character]:
    from_point = random.randint(0, CHROMOSOME_LENGTH - 1)
    amount = random.randint(0, math.ceil(CHROMOSOME_LENGTH / 2))

    return __cross_parents(parent1, parent2, from_point, amount)


# Selects a random point in the chromosome and crosses the genes from that point
def __point(parent1: Character, parent2: Character) -> Tuple[Character, Character]:
    from_point = random.randint(0, CHROMOSOME_LENGTH - 1)
    amount = CHROMOSOME_LENGTH - from_point

    return __cross_parents(parent1, parent2, from_point, amount)


# Selects two random points in the chromosome and crosses the genes between them
def __two_point(parent1: Character, parent2: Character) -> Tuple[Character, Character]:
    from_point = random.randint(0, CHROMOSOME_LENGTH - 1)
    to_point = random.randint(0, CHROMOSOME_LENGTH - 1)
    if from_point > to_point:
        from_point, to_point = to_point, from_point

    amount = to_point - from_point

    return __cross_parents(parent1, parent2, from_point, amount)


# For each gene, it has a probability of crossing it
uniform_crossover_probability: float
def __uniform(parent1: Character, parent2: Character) -> Tuple[Character, Character]:
    child1 = Character(parent1.chromosome.copy())
    child2 = Character(parent2.chromosome.copy())

    global uniform_crossover_probability
    for i in range(CHROMOSOME_LENGTH):
        if random.random() < uniform_crossover_probability:
            child1.chromosome[i] = parent2.chromosome[i]
            child2.chromosome[i] = parent1.chromosome[i]

    return child1, child2


# --------------------- Builder --------------------- #

CrossOverMethod = Callable[[list[Character]], list[Character]]
__crossover_methods: Dict[str, CrossOverMethod] = {
    "anular": lambda population: __cross_population(population, __anular),
    "point": lambda population: __cross_population(population, __point),
    "two_point": lambda population: __cross_population(population, __two_point),
    "uniform": lambda population: __cross_population(population, __uniform),
}

def get_crossover_method(crossover_config: dict) -> CrossOverMethod:
    crossover_method = crossover_config["crossover_method"]
    if crossover_method not in __crossover_methods:
        raise ValueError(f"Unknown crossover method: {crossover_method}")

    if crossover_method == "uniform":
        global uniform_crossover_probability
        uniform_crossover_probability = crossover_config["crossover_probability"]


    return __crossover_methods[crossover_method]

# --------------------- Helpers --------------------- #

# Crosses the population using the given method
# If the population is odd, the last individual is not crossed
def __cross_population(
    population: list[Character],
    method: Callable[[Character, Character], Tuple[Character, Character]],
) -> list[Character]:
    amount_to_cross = (
        len(population) if len(population) % 2 == 0 else len(population) - 1
    )

    children = []
    for i in range(0, amount_to_cross, 2):
        child1, child2 = method(population[i], population[i + 1])

        children.append(child1)
        children.append(child2)

    return children

# Crosses the parents from the given point and amount
def __cross_parents(
    parent1: Character, parent2: Character, from_point: int, amount: int
) -> Tuple[Character, Character]:
    child1 = Character(parent1.chromosome.copy())
    child2 = Character(parent2.chromosome.copy())

    for i in range(amount):
        index = (from_point + i) % CHROMOSOME_LENGTH
        child1.chromosome[index] = parent2.chromosome[index]
        child2.chromosome[index] = parent1.chromosome[index]

    return child1, child2

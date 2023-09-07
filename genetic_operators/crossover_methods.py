import math
import random
from individual.character import Character
from individual.character import normalize_points
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
def __uniform(
    parent1: Character, parent2: Character, crossover_probability: float
) -> Tuple[Character, Character]:
    child1 = Character(parent1.chromosome.copy())
    child2 = Character(parent2.chromosome.copy())

    for i in range(CHROMOSOME_LENGTH):
        if random.random() < crossover_probability:
            child1.chromosome[i] = parent2.chromosome[i]
            child2.chromosome[i] = parent1.chromosome[i]

    return child1, child2


# --------------------- Builder --------------------- #

CrossOverMethod = Callable[[list[Character]], list[Character]]
__crossover_methods: Dict[str, Callable] = {
    "anular": __anular,
    "point": __point,
    "two_point": __two_point,
    "uniform": __uniform,
}


# Builds the crossover method from the given config
def get_crossover_method(crossover_config: dict) -> CrossOverMethod:
    crossover_method = crossover_config["method"]

    if crossover_method not in __crossover_methods:
        raise ValueError(f"Unknown crossover method: {crossover_method}")

    # Uniform crossover is a special case, since it needs a probability
    if crossover_method == "uniform":
        uniform_crossover_probability = crossover_config["crossover_probability"]

        if uniform_crossover_probability < 0 or uniform_crossover_probability > 1:
            raise ValueError(
                f"Invalid crossover probability: {uniform_crossover_probability}"
            )

        # Build the uniform crossover method with the given probability
        crossover_method = lambda p1, p2: __uniform(
            p1, p2, uniform_crossover_probability
        )
    else:
        crossover_method = __crossover_methods[crossover_method]

    # Build the crossover method with the given method
    return lambda population: __cross_population(population, crossover_method)


# --------------------- Helpers --------------------- #


# Crosses the population using the given method
# If the population is odd, the last individual is not crossed
def __cross_population(
    population: list[Character],
    method: Callable[[Character, Character], Tuple[Character, Character]],
) -> list[Character]:
    random.shuffle(population)
    population_length = len(population)

    children = []
    for i in range(0, population_length, 2):
        child1, child2 = method(
            population[i % population_length], population[(i + 1) % population_length]
        )

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

    normalize_points(child1.chromosome)
    normalize_points(child2.chromosome)
    return child1, child2

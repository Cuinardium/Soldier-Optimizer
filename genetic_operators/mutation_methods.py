import random
from typing import Callable
from individual.character import Character, normalize_points

mutation_probability: float
initial_mutation_probability: float

# --------------------- Methods --------------------- #


def single_gen_mutation(
    individual: Character, gen: Character.Characteristics, mutation_probability: float
) -> Character:
    if random.random() < mutation_probability:
        __mutate_gen(individual.chromosome, gen)

    return individual


def multi_gen_mutation(individual: Character, mutation_probability: float) -> Character:
    for characteristic in Character.Characteristics:
        if random.random() < mutation_probability:
            __mutate_gen(individual.chromosome, characteristic)
    return individual


# --------------------- Builder --------------------- #

MutationMethod = Callable[[list[Character]], list[Character]]


# Builds the mutation method from thr given config
def get_mutation_method(config: dict) -> MutationMethod:
    # Set the mutation probability
    global mutation_probability
    global initial_mutation_probability
    mutation_probability = config["probability"]
    initial_mutation_probability = mutation_probability

    if mutation_probability < 0 or mutation_probability > 1:
        raise ValueError("Mutation probability must be between 0 and 1 (inclusive)")

    gen_to_mutate = Character.Characteristics.from_string(
        config["single_gen"]["gen_to_mutate"]
    )

    mutation_probability_descent_rate = config["non_uniform"]["descent_rate"]
    if mutation_probability_descent_rate < 0 or mutation_probability_descent_rate > 1:
        raise ValueError(
            "Mutation probability descent rate must be between 0 and 1 (inclusive)"
        )

    return lambda population: __mutate_population(
        population,
        config["multi_gen"],
        config["uniform"],
        gen_to_mutate,
        mutation_probability_descent_rate,
    )


# --------------------- Helpers --------------------- #


def __mutate_population(
    population: list[Character],
    multi_gen: bool,
    uniform: bool,
    gen_to_mutate: Character.Characteristics,
    mutation_probability_descent_rate: float,
) -> list[Character]:
    global mutation_probability

    for index, individual in enumerate(population):
        if multi_gen:
            population[index] = multi_gen_mutation(individual, mutation_probability)
        else:
            population[index] = single_gen_mutation(
                individual, gen_to_mutate, mutation_probability
            )

    if not uniform:
        # Reduce mutation probability
        mutation_probability *= 1 - mutation_probability_descent_rate

    return population


def __mutate_gen(chromosome: list[float], gen: Character.Characteristics):
    if gen == Character.Characteristics.HEIGHT:
        chromosome[gen.value] = random.uniform(1.3, 2.0)
        return chromosome

    chromosome[gen.value] = random.uniform(0, 150)

    # Normalize points so that the sum of all points is 150
    normalize_points(chromosome)


def reset_mutation_globals():
    global mutation_probability
    global initial_mutation_probability
    mutation_probability = initial_mutation_probability

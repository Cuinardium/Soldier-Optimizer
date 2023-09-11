from typing import Tuple
from genetic_operators.crossover_methods import CrossOverMethod
from genetic_operators.mutation_methods import MutationMethod
from genetic_operators.selection_methods import SelectionMethod
from individual.character import Character, random_individual
from individual.fitness import FitnessFunction
from stop_criteria import StopCriteria


def simulate(
    fitness_function: FitnessFunction,
    selection_method: SelectionMethod,
    crossover_method: CrossOverMethod,
    mutation_method: MutationMethod,
    replacement_method: SelectionMethod,
    stop_criteria: StopCriteria,
    population_size: int,
) -> Tuple[list[Character], int]:
    population = [random_individual() for _ in range(population_size)]

    # Run the simulation until the stop criteria is met
    iterations = 0
    while True:
        # Select individuals for crossover
        parents = selection_method(population, fitness_function)

        # Create new individuals by crossover and mutate them
        children = crossover_method(parents)
        children = mutation_method(children)

        # Replace the old population with the new population
        old_population = population
        population = replacement_method(population + children, fitness_function)

        if stop_criteria(population, old_population, iterations, fitness_function):
            break

        iterations += 1

    return population, iterations + 1


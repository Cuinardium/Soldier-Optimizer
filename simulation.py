from genetic_operators.crossover_methods import CrossOverMethod
from genetic_operators.mutation_methods import MutationMethod
from genetic_operators.selection_methods import SelectionMethod
from individual.character import Character, random_individual
from individual.fitness import FitnessFunction


def simulate(
    fitness_function: FitnessFunction,
    selection_method: SelectionMethod,
    crossover_method: CrossOverMethod,
    mutation_method: MutationMethod,
    replacement_method: SelectionMethod,
    stop_criteria,
    population_size: int,
):
    population = initialize_population(population_size)

    # Run the simulation until the stop criteria is met
    iterations = 0
    while not stop_criteria(population, iterations):
        # Select individuals for crossover
        parents = selection_method(population, fitness_function)

        # Create new individuals by crossover and mutate them
        children = crossover_method(parents)
        children = mutation_method(children)

        # Replace the old population with the new population
        population = replacement_method(population + children, fitness_function)

        iterations += 1

    return population


def initialize_population(population_size: int) -> list[Character]:
    population = []

    # Create a random individual for each index in the population
    for _ in range(population_size):
        population.append(random_individual())

    return population

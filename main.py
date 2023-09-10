import json

from individual.fitness import get_class_fitness_function

from genetic_operators.selection_methods import get_selection_method
from genetic_operators.crossover_methods import get_crossover_method
from genetic_operators.mutation_methods import get_mutation_method

from stop_criteria import get_stop_criteria

from simulation import simulate


def main():
    with open("config.json") as config_file:
        config = json.load(config_file)

        # Load config
        fitness_function = get_class_fitness_function(config["character_class"])

        selection_method = get_selection_method(config["selection"])
        crossover_method = get_crossover_method(config["crossover"])
        mutation_method = get_mutation_method(config["mutation"])
        replacement_method = get_selection_method(config["replacement"])

        stop_criteria = get_stop_criteria(config["stop_criteria"])

        population_size = config["population_size"]

        # Run simulation
        final_population, iterations = simulate(
            fitness_function,
            selection_method,
            crossover_method,
            mutation_method,
            replacement_method,
            stop_criteria,
            population_size,
        )

        # Print results
        print("Final population:")
        for individual in final_population:
            print(individual)
            print(f"Fitness: {fitness_function(individual)}\n")

        print(f"Number of iterations: {iterations}")


if __name__ == "__main__":
    main()

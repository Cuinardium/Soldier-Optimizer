import json

from individual.fitness import fitness_functions
from genetic_operators.selection_methods import get_selection_method
from genetic_operators.crossover_methods import get_crossover_method
from genetic_operators.mutation_methods import get_mutation_method

from simulation import simulate

stop_criteria_methods = {}


def main():
    with open("config.json") as config_file:
        config = json.load(config_file)

        # ------------ Class ------------
        character_class = config["character_class"]
        if character_class not in fitness_functions:
            raise ValueError(f"Unknown character class: {character_class}")
        fitness_function = fitness_functions[character_class]

        # ------------ Genetic Operators ------------
        selection_method = get_selection_method(config["selection"])
        crossover_method = get_crossover_method(config["crossover"])
        mutation_method = get_mutation_method(config["mutation"])
        replacement_method = get_selection_method(config["replacement"])

        # ------------ Stop Criteria ------------
        stop_criteria = config["stop_criteria"]
        if stop_criteria not in stop_criteria_methods:
            raise ValueError(f"Unknown stop criteria: {stop_criteria}")
        stop_criteria = stop_criteria_methods[stop_criteria]

        # ------------ Population ------------
        population_size = config["population_size"]

        # ------------ Simulation ------------
        final_population = simulate(
            fitness_function,
            selection_method,
            crossover_method,
            mutation_method,
            replacement_method,
            stop_criteria,
            population_size,
        )

        # ------------ Results ------------
        print("Final population:")
        for individual in final_population:
            print(individual)
            print(f"Fitness: {fitness_function(individual)}\n")


if __name__ == "__main__":
    main()

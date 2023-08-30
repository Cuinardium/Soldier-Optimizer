import json
from simulation import simulate
from individual.fitness import (
    warrior_fitness,
    archer_fitness,
    defender_fitness,
    infiltrator_fitness,
)

fitness_functions = {
    "warrior": warrior_fitness,
    "archer": archer_fitness,
    "defender": defender_fitness,
    "infiltrator": infiltrator_fitness,
}

crossover_methods = {}

mutation_methods = {}

selection_methods = {}

stop_criteria_methods = {}


def main():
    with open("config.json") as config_file:
        config = json.load(config_file)

        # ------------ Class ------------
        character_class = config["character_class"]
        if character_class not in fitness_functions:
            raise ValueError(f"Unknown character class: {character_class}")
        fitness_function = fitness_functions[character_class]

        # ------------ Crossover ------------
        crossover_method = config["crossover_method"]
        if crossover_method not in crossover_methods:
            raise ValueError(f"Unknown crossover method: {crossover_method}")
        crossover_method = crossover_methods[crossover_method]

        # ------------ Mutation ------------
        mutation_method = config["mutation_method"]
        if mutation_method not in mutation_methods:
            raise ValueError(f"Unknown mutation method: {mutation_method}")
        mutation_method = mutation_methods[mutation_method]

        # ------------ Selection ------------
        selection_method1 = config["selection_method1"]
        if selection_method1 not in selection_methods:
            raise ValueError(f"Unknown selection method: {selection_method1}")
        selection_method1 = selection_methods[selection_method1]

        selection_method2 = config["selection_method2"]
        if selection_method2 not in selection_methods:
            raise ValueError(f"Unknown selection method: {selection_method2}")
        selection_method2 = selection_methods[selection_method2]

        a_weight = config["a_weight"]

        def selection_method():
            return selection_method1() * a_weight + selection_method2() * (1 - a_weight)

        # ----------- Replacement ------------
        replacement_method1 = config["replacement_method1"]
        if replacement_method1 not in selection_methods:
            raise ValueError(f"Unknown replacement method: {replacement_method1}")
        replacement_method1 = selection_methods[replacement_method1]

        replacement_method2 = config["replacement_method2"]
        if replacement_method2 not in selection_methods:
            raise ValueError(f"Unknown replacement method: {replacement_method2}")
        replacement_method2 = selection_methods[replacement_method2]

        b_weight = config["b_weight"]

        def replacement_method():
            return replacement_method1() * b_weight + (
                replacement_method2() * (1 - b_weight)
            )

        # ------------ Stop Criteria ------------
        stop_criteria = config["stop_criteria"]
        if stop_criteria not in stop_criteria_methods:
            raise ValueError(f"Unknown stop criteria: {stop_criteria}")
        stop_criteria = stop_criteria_methods[stop_criteria]

        # ------------ Population ------------
        population_size = config["population_size"]

        # ------------ Simulation ------------
        simulate(
            fitness_function,
            crossover_method,
            mutation_method,
            selection_method,
            replacement_method,
            stop_criteria,
            population_size,
        )


if __name__ == "__main__":
    main()

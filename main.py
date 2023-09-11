import json
import csv
from pathlib import Path

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

        iterations = config["iterations"]

        test_name = config["test_name"]

        # Run simulation
        print(f"Running {test_name}")

        simulation_results = []
        for _ in range(iterations):
            print(f"Running iteration {_ + 1} of {iterations}")

            final_population, generations = simulate(
                fitness_function,
                selection_method,
                crossover_method,
                mutation_method,
                replacement_method,
                stop_criteria,
                population_size,
            )

            best_individual = max(
                final_population, key=lambda individual: fitness_function(individual)
            )
            simulation_results.append((best_individual, generations))

            print(f"Best individual: {best_individual}")
            print(f"Fitness: {fitness_function(best_individual)}")
            print(f"Generations: {generations}")

        # Save results
        test_dir = Path(f"results/{test_name}")
        test_dir.mkdir(parents=True, exist_ok=True)

        with open(test_dir / "config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)

        with open(test_dir / "results.csv", "w") as results_file:
            results_writer = csv.writer(results_file)

            results_writer.writerow(
                [
                    "strength",
                    "agility",
                    "expertise",
                    "resistance",
                    "health",
                    "height",
                    "fitness",
                    "generations",
                ]
            )

            for individual, generations in simulation_results:
                results_writer.writerow(
                    [
                        individual.get_strength_points(),
                        individual.get_agility_points(),
                        individual.get_expertise_points(),
                        individual.get_resistance_points(),
                        individual.get_health_points(),
                        individual.get_height(),
                        fitness_function(individual),
                        generations,
                    ]
                )


if __name__ == "__main__":
    main()

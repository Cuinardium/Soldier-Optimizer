from typing import Callable, Dict, List

from individual.character import Character
from individual.fitness import FitnessFunction

# -------------- Stop Criteria -------------- #


def __max_generations(max_generations: int, current_generation: int) -> bool:
    return current_generation >= max_generations


def __expected_fitness(
    expected_fitness: float,
    population: List[Character],
    fitness_function: FitnessFunction,
) -> bool:
    for individual in population:
        if fitness_function(individual) >= expected_fitness:
            return True
    return False


fitness_similar_generations = 0


def __population_fitness_convergence(
    population: List[Character],
    previous_population: List[Character],
    fitness_function: FitnessFunction,
    fitness_convergence_delta: float,
    similar_generations_threshold: int,
) -> bool:
    global fitness_similar_generations

    population_best_fitness = max(
        fitness_function(individual) for individual in population
    )
    previous_population_best_fitness = max(
        fitness_function(individual) for individual in previous_population
    )

    if (
        abs(population_best_fitness - previous_population_best_fitness)
        > fitness_convergence_delta
        or previous_population_best_fitness == -1
    ):
        previous_population_best_fitness = population_best_fitness
        fitness_similar_generations = 0
        return False

    fitness_similar_generations += 1

    return fitness_similar_generations >= similar_generations_threshold


structure_similar_generations = 0


def __population_structure_convergence(
    population: List[Character],
    previous_population: List[Character],
    convergence_deltas: Dict[Character.Characteristics, float],
    similar_generations_threshold: int,
    similar_individuals_proportion: float,
) -> bool:
    characteristics_to_analyze = convergence_deltas.keys()

    def __match(individual: Character, other_individual: Character) -> bool:
        for characteristic in characteristics_to_analyze:
            if (
                abs(
                    individual.chromosome[characteristic.value]
                    - other_individual.chromosome[characteristic.value]
                )
                > convergence_deltas[characteristic]
            ):
                return False
        return True

    global structure_similar_generations
    similar_individuals = 0
    for individual in population:
        for previous_individual in previous_population:
            if __match(individual, previous_individual):
                similar_individuals += 1
                break

    if similar_individuals >= similar_individuals_proportion * len(population):
        structure_similar_generations += 1
    else:
        structure_similar_generations = 0

    return structure_similar_generations >= similar_generations_threshold


# -------------- Build ---------------------- #

StopCriteria = Callable[[List[Character], List[Character], int, FitnessFunction], bool]


def get_stop_criteria(config: dict) -> StopCriteria:
    criteria = config["criteria"]

    if criteria == "generations":
        generations_config = config["generations"]
        max_generations = generations_config["max_generations"]

        return lambda population, previous_population, generations, fitness_function: __max_generations(
            max_generations, generations
        )
    if criteria == "fitness":
        fitness_config = config["fitness"]
        expected_fitness = fitness_config["expected_fitness"]

        return lambda population, previous_population, generations, fitness_function: __expected_fitness(
            expected_fitness, population, fitness_function
        )
    if criteria == "fitness_convergence":
        fitness_convergence_config = config["fitness_convergence"]
        fitness_convergence_delta = fitness_convergence_config["fitness_delta"]
        similar_generations_threshold = fitness_convergence_config[
            "similar_generations_threshold"
        ]

        return lambda population, previous_population, generations, fitness_function: __population_fitness_convergence(
            population,
            previous_population,
            fitness_function,
            fitness_convergence_delta,
            similar_generations_threshold,
        )
    if criteria == "structure_convergence":
        structure_convergence_config = config["structure_convergence"]
        similar_generations_threshold = structure_convergence_config[
            "similar_generations_threshold"
        ]
        similar_individuals_proportion = structure_convergence_config[
            "similar_individuals_proportion"
        ]

        deltas: Dict[Character.Characteristics, float] = {}

        for characteristic_name, delta in structure_convergence_config["deltas"].items():
            if delta is None:
                continue

            characteristic = Character.Characteristics.from_string(characteristic_name)
            deltas[characteristic] = delta

        return lambda population, previous_population, generations, fitness_function: __population_structure_convergence(
            population,
            previous_population,
            deltas,
            similar_generations_threshold,
            similar_individuals_proportion,
        )

        

    raise ValueError(f"Invalid stop criteria: {criteria}")

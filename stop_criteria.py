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


def __population_fitness_convergence(
    population: List[Character],
    old_population: List[Character],
    fitness_function: FitnessFunction,
    fitness_convergence_delta: float,
) -> bool:
    population_fitness = sum(
        fitness_function(individual) for individual in population
    ) / len(population)
    old_population_fitness = sum(
        fitness_function(individual) for individual in old_population
    ) / len(old_population)

    fitness_delta = abs(population_fitness - old_population_fitness)

    return fitness_delta <= fitness_convergence_delta


def __population_structure_convergence(
    population: List[Character],
    old_population: List[Character],
    convergence_deltas: Dict[Character.Characteristics, float],
) -> bool:
    characteristics_to_analyze = convergence_deltas.keys()

    for characteristic in characteristics_to_analyze:
        population_characteristic_avg = sum(
            individual.chromosome[characteristic.value] for individual in population
        ) / len(population)
        old_population_characteristic_avg = sum(
            individual.chromosome[characteristic.value] for individual in old_population
        ) / len(old_population)

        characteristic_delta = abs(
            population_characteristic_avg - old_population_characteristic_avg
        )

        if characteristic_delta > convergence_deltas[characteristic]:
            return False

    return True


# -------------- Build ---------------------- #

StopCriteria = Callable[[List[Character], List[Character], int, FitnessFunction], bool]


def get_stop_criteria(config: dict) -> StopCriteria:
    criteria = config["criteria"]

    if criteria == "generations":
        generations_config = config["generations"]
        max_generations = generations_config["max_generations"]

        return lambda population, old_population, generations, fitness_function: __max_generations(
            max_generations, generations
        )
    if criteria == "fitness":
        fitness_config = config["fitness"]
        expected_fitness = fitness_config["expected_fitness"]

        return lambda population, old_population, generations, fitness_function: __expected_fitness(
            expected_fitness, population, fitness_function
        )
    if criteria == "fitness_convergence":
        fitness_convergence_config = config["fitness_convergence"]
        fitness_convergence_delta = fitness_convergence_config["fitness_delta"]

        return lambda population, old_population, generations, fitness_function: __population_fitness_convergence(
            population, old_population, fitness_function, fitness_convergence_delta
        )
    if criteria == "structure_convergence":
        structure_convergence_config: Dict[str, float] = config["structure_convergence"]

        deltas: Dict[Character.Characteristics, float] = {}

        for key, delta in structure_convergence_config.items():
            if delta is None:
                continue

            # Remove _delta from string
            characteristic_name = key.replace("_delta", "")

            characteristic = Character.Characteristics.from_string(characteristic_name)
            deltas[characteristic] = delta

            return lambda population, old_population, generations, fitness_function: __population_structure_convergence(
                population, old_population, deltas
            )

    raise ValueError(f"Invalid stop criteria: {criteria}")

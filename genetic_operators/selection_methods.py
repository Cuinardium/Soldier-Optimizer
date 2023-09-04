from typing import Callable, Dict
from individual.character import Character
from individual.fitness import FitnessFunction


def elitism(
    population: list[Character], fitness_function: FitnessFunction
) -> list[Character]:
    return population


def roulette(
    population: list[Character], fitness_function: FitnessFunction
) -> list[Character]:
    return population


def universal(
    population: list[Character], fitness_function: FitnessFunction
) -> list[Character]:
    return population


def boltzmann(
    population: list[Character], fitness_function: FitnessFunction
) -> list[Character]:
    return population


def tournament(
    population: list[Character], fitness_function: FitnessFunction
) -> list[Character]:
    return population


def ranking(
    population: list[Character], fitness_function: FitnessFunction
) -> list[Character]:
    return population


SelectionMethod = Callable[[list[Character], FitnessFunction], list[Character]]

selection_methods: Dict[str, SelectionMethod] = {
    "elitism": elitism,
    "roulette": roulette,
    "universal": universal,
    "boltzmann": boltzmann,
    "ranking": ranking,
    "tournament": tournament,
}


def join_selection_methods(
    selection_method_1: SelectionMethod,
    selection_method_2: SelectionMethod,
    method_1_weight: float,
) -> SelectionMethod:
    def joined_selection_method(
        population: list[Character], fitness_function: FitnessFunction
    ) -> list[Character]:
        amount_1 = int(len(population) * method_1_weight)

        return (
            selection_method_1(population[:amount_1], fitness_function)
            + selection_method_2(population[amount_1:], fitness_function)
        )

    return joined_selection_method

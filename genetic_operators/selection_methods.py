from typing import Callable
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

selection_methods = {
    "elitism": elitism,
    "roulette": roulette,
    "universal": universal,
    "boltzmann": boltzmann,
    "ranking": ranking,
    "tournament": tournament,
}

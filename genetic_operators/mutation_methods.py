from typing import Callable, Dict
from individual.character import Character

def gen(population: list[Character]) -> list[Character]:
    return population

def multi_gen(population: list[Character]) -> list[Character]:
    return population

def not_uniform(population: list[Character]) -> list[Character]:
    return population

def uniform(population: list[Character]) -> list[Character]:
    return population

MutationMethod = Callable[[list[Character]], list[Character]]

mutation_methods: Dict[str, MutationMethod] = {
    "gen": gen,
    "multi_gen": multi_gen,
    "not_uniform": not_uniform,
    "uniform": uniform,
}

from individual.character import Character
from typing import Callable


def warrior_fitness(character: Character) -> float:
    return 0.6 * character.get_attack() + 0.4 * character.get_defense()


def archer_fitness(character: Character) -> float:
    return 0.9 * character.get_attack() + 0.1 * character.get_defense()


def defender_fitness(character: Character) -> float:
    return 0.1 * character.get_attack() + 0.9 * character.get_defense()


def infiltrator_fitness(character: Character) -> float:
    return 0.7 * character.get_attack() + 0.3 * character.get_defense()

FitnessFunction = Callable[[Character], float]

fitness_functions = {
    "warrior": warrior_fitness,
    "archer": archer_fitness,
    "defender": defender_fitness,
    "infiltrator": infiltrator_fitness,
}

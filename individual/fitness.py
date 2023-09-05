from individual.character import Character
from typing import Callable


def __warrior_fitness(character: Character) -> float:
    return 0.6 * character.get_attack() + 0.4 * character.get_defense()


def __archer_fitness(character: Character) -> float:
    return 0.9 * character.get_attack() + 0.1 * character.get_defense()


def __defender_fitness(character: Character) -> float:
    return 0.1 * character.get_attack() + 0.9 * character.get_defense()


def __infiltrator_fitness(character: Character) -> float:
    return 0.7 * character.get_attack() + 0.3 * character.get_defense()


FitnessFunction = Callable[[Character], float]
__fitness_functions = {
    "warrior": __warrior_fitness,
    "archer": __archer_fitness,
    "defender": __defender_fitness,
    "infiltrator": __infiltrator_fitness,
}


def get_class_fitness_function(character_class: str) -> FitnessFunction:
    if character_class not in __fitness_functions:
        raise ValueError(f"Unknown character class: {character_class}")

    return __fitness_functions[character_class]

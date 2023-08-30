from character import Character

def warrior_fitness(character: Character) -> float:
    return 0.6 * character.get_attack() + 0.4 * character.get_defense()


def archer_fitness(character: Character) -> float:
    return 0.9 * character.get_attack() + 0.1 * character.get_defense()


def defender_fitness(character: Character) -> float:
    return 0.1 * character.get_attack() + 0.9 * character.get_defense()


def infiltrator_fitness(character: Character) -> float:
    return 0.7 * character.get_attack() + 0.3 * character.get_defense()

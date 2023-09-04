import math
from enum import Enum
import random


class Character:
    class Characteristics(Enum):
        STRENGTH = 0
        AGILITY = 1
        EXPERTISE = 2
        RESISTANCE = 3
        HEALTH = 4
        HEIGHT = 5

    def __init__(self, chromosome: list[float]):
        self.chromosome = chromosome

    # -------- Encoded in chromosome -------- #

    def get_strength_points(self) -> float:
        return self.chromosome[Character.Characteristics.STRENGTH.value]

    def get_agility_points(self) -> float:
        return self.chromosome[Character.Characteristics.AGILITY.value]

    def get_expertise_points(self) -> float:
        return self.chromosome[Character.Characteristics.EXPERTISE.value]

    def get_resistance_points(self) -> float:
        return self.chromosome[Character.Characteristics.RESISTANCE.value]

    def get_health_points(self) -> float:
        return self.chromosome[Character.Characteristics.HEALTH.value]

    def get_height(self) -> float:
        return self.chromosome[Character.Characteristics.HEIGHT.value]

    # ------- Coefficients -------- #

    def get_strength_coefficient(self) -> float:
        return 100 * math.tanh(0.01 * self.get_strength_points())

    def get_agility_coefficient(self) -> float:
        return math.tanh(0.01 * self.get_agility_points())

    def get_expertise_coefficient(self) -> float:
        return 0.6 * math.tanh(0.01 * self.get_expertise_points())

    def get_resistance_coefficient(self) -> float:
        return math.tanh(0.01 * self.get_resistance_points())

    def get_health_coefficient(self) -> float:
        return 100 * math.tanh(0.01 * self.get_health_points())

    # ------- Attack and Defense modifiers -------- #

    def get_attack_modifier(self) -> float:
        height = self.get_height()
        return 0.5 - (3 * height - 5) ** 4 + (3 * height - 5) ** 2 + height / 2

    def get_defense_modifier(self):
        height = self.get_height()
        return 2 + (3 * height - 5) ** 4 - (3 * height - 5) ** 2 - height / 2

    # ------- Attack and Defense -------- #

    def get_attack(self) -> float:
        return (
            (self.get_agility_coefficient() + self.get_expertise_coefficient())
            * self.get_strength_coefficient()
            * self.get_attack_modifier()
        )

    def get_defense(self) -> float:
        return (
            (self.get_resistance_coefficient() + self.get_expertise_coefficient())
            * self.get_health_coefficient()
            * self.get_defense_modifier()
        )

    # ------- String representation -------- #
    def __str__(self) -> str:
        return (
            f"Character: \n"
            f"Strength: {self.get_strength_points()} \n"
            f"Agility: {self.get_agility_points()} \n"
            f"Expertise: {self.get_expertise_points()} \n"
            f"Resistance: {self.get_resistance_points()} \n"
            f"Health: {self.get_health_points()} \n"
            f"Height: {self.get_height()} \n"
            f"Attack: {self.get_attack()} \n"
            f"Defense: {self.get_defense()} \n"
        )


# Create a random individual
def random_individual() -> Character:
    chromosome: list[float] = []

    # Height must be between 1.3 and 2.0
    chromosome[Character.Characteristics.HEIGHT.value] = random.uniform(1.3, 2.0)

    # Strength, agility, expertise, resistance, health, normal distribution
    # mean = 150/5 = 30, standard deviation = 30/5 = 6
    for characteristic in Character.Characteristics:
        chromosome[characteristic.value] = random.gauss(30, 6)

    normalize_points(chromosome)

    return Character(chromosome)


def normalize_points(chromosome: list[float]):
    sum_points = 0.0
    for characteristic in Character.Characteristics:
        sum_points += chromosome[characteristic.value]

    for characteristic in Character.Characteristics:
        chromosome[characteristic.value] = (
            chromosome[characteristic.value] / sum_points * 150
        )

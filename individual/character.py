from abc import abstractmethod
import math
from enum import Enum


class Character:
    class Characteristics(Enum):
        STRENGTH = 0
        AGILITY = 1
        EXPERTISE = 2
        RESISTANCE = 3
        HEALTH = 4
        HEIGHT = 5

    def __init__(self, chromosome):
        self.chromosome = chromosome

    # -------- Encoded in chromosome -------- #

    def get_strength_points(self):
        return self.chromosome[Character.Characteristics.STRENGTH.value]

    def get_agility_points(self):
        return self.chromosome[Character.Characteristics.AGILITY.value]

    def get_expertise_points(self):
        return self.chromosome[Character.Characteristics.EXPERTISE.value]

    def get_resistance_points(self):
        return self.chromosome[Character.Characteristics.RESISTANCE.value]

    def get_health_points(self):
        return self.chromosome[Character.Characteristics.HEALTH.value]

    def get_height(self):
        return self.chromosome[Character.Characteristics.HEIGHT.value]

    # ------- Coefficients -------- #

    def get_strength_coefficient(self):
        return 100 * math.tanh(0.01 * self.get_strength_points())

    def get_agility_coefficient(self):
        return math.tanh(0.01 * self.get_agility_points())

    def get_expertise_coefficient(self):
        return 0.6 * math.tanh(0.01 * self.get_expertise_points())

    def get_resistance_coefficient(self):
        return math.tanh(0.01 * self.get_resistance_points())

    def get_health_coefficient(self):
        return 100 * math.tanh(0.01 * self.get_health_points())

    # ------- Attack and Defense modifiers -------- #

    def get_attack_modifier(self):
        height = self.get_height()
        return 0.5 - (3 * height - 5) ** 4 + (3 * height - 5) ** 2 + height / 2

    def get_defense_modifier(self):
        height = self.get_height()
        return 2 + (3 * height - 5) ** 4 - (3 * height - 5) ** 2 - height / 2

    # ------- Attack and Defense -------- #

    def get_attack(self):
        return (
            (self.get_agility_coefficient() + self.get_expertise_coefficient())
            * self.get_strength_coefficient()
            * self.get_attack_modifier()
        )

    def get_defense(self):
        return (
            (self.get_resistance_coefficient() + self.get_expertise_coefficient())
            * self.get_health_coefficient()
            * self.get_defense_modifier()
        )

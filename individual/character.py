from abc import abstractmethod
import math


class Character:
    def __init__(self, chromosome):
        self.chromosome = chromosome

    # -------- Encoded in chromosome TODO: implement -------- #

    def get_strength_points(self):
        pass

    def get_agility_points(self):
        pass

    def get_expertise_points(self):
        pass

    def get_resistance_points(self):
        pass

    def get_health_points(self):
        pass

    def get_height(self):
        pass

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

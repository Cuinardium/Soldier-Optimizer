from typing import Callable, Dict
from individual.character import Character
from individual.fitness import FitnessFunction
import random


def elitism(
    population: list[Character], fitness_function: FitnessFunction
) -> list[Character]:
    return population

# TODO: ver si le pasamos cantidad a seleccionar
def roulette(
    population: list[Character], fitness_function: FitnessFunction, num_selections : int
) -> list[Character]:
    
    # Calcula la suma total de aptitudes de todos los individuos. TODO funcion para calcular fitness
    total_fitness = sum(character.fitness for character in population)
    
    cumulative_probabilities = []
    cumulative_probability = 0.0
    
    # Calcula las probabilidades acumulativas para cada individuo
    for character in population:
        # Calcula la probabilidad relativa de selección para este individuo
        probability = character.fitness / total_fitness
        
        # Agrega la probabilidad acumulativa a la lista
        cumulative_probability += probability
        cumulative_probabilities.append(cumulative_probability)
        
    # Realiza las selecciones especificadas
    selections = []
    for _ in range(num_selections):
        random_value = random.random()
        
        # Encuentra el individuo correspondiente al valor aleatorio
        selected_individual = None
        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if random_value <= cumulative_probability:
                selected_individual = population[i]
                break
        
        if selected_individual is not None:
            selections.append(selected_individual)
    
    return selections


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

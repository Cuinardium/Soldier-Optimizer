import copy
import functools
from typing import Callable, Dict
from individual.character import Character
from individual.fitness import FitnessFunction
import random


# --------------------- Methods --------------------- #


def __elitism(
        population: list[Character],
        fitness_function: FitnessFunction,
        selection_amount: int,
) -> list[Character]:
    return population


def __roulette(
        population: list[Character],
        fitness_function: FitnessFunction,
        selection_amount: int,
) -> list[Character]:
    # Calcula la suma total de aptitudes de todos los individuos.
    total_fitness = sum(fitness_function(character) for character in population)

    cumulative_probabilities = []
    cumulative_probability = 0.0

    # Calcula las probabilidades acumulativas para cada individuo
    for character in population:
        # Calcula la probabilidad relativa de selección para este individuo
        probability = fitness_function(character) / total_fitness

        # Agrega la probabilidad acumulativa a la lista
        cumulative_probability += probability
        cumulative_probabilities.append(cumulative_probability)

    # Realiza las selecciones especificadas
    selections = []
    for _ in range(selection_amount):
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


def __universal(
        population: list[Character],
        fitness_function: FitnessFunction,
        selection_amount: int,
) -> list[Character]:
    return population


def __boltzmann(
        population: list[Character],
        fitness_function: FitnessFunction,
        selection_amount: int,
) -> list[Character]:
    return population


def __tournament(
        population: list[Character],
        fitness_function: FitnessFunction,
        selection_amount: int,
) -> list[Character]:
    return population

# TODO El threshold deberia ser parametrizable? 
def __tournament_probabilistic(
    population: list[Character],
    fitness_function: FitnessFunction,
    selection_amount: int,
) -> list[Character]:
    
    threshold = 0.75
    selections = []
    
    for _ in range(selection_amount):
        
        random_probability = random.random()
        tournament= random.sample(population, 2)
        
        if(random_probability<threshold):
            selections.append( max(tournament, key=fitness_function) )
        else:
            selections.append( min(tournament, key=fitness_function) )
            
    
    return selections


def __ranking(
        population: list[Character],
        fitness_function: FitnessFunction,
        selection_amount: int,
) -> list[Character]:
    ranked_list = copy.copy(population)

    ranked_list.sort(key=functools.cmp_to_key(lambda x, y: compare(x, y, fitness_function)))

    size = len(ranked_list)

    #TODO: ver si seria mejor crear un dict character -> ranking
    # para agilizar la obtencion del puesto
    # (no usar index de la ranked_list)

    return __roulette(population,
                      lambda character: (size - ranked_list.index(character)) / size,
                      selection_amount)


# --------------------- Builder --------------------- #

SelectionMethod = Callable[[list[Character], FitnessFunction], list[Character]]
__selection_methods: Dict[str, Callable] = {
    "elitism": __elitism,
    "roulette": __roulette,
    "universal": __universal,
    "boltzmann": __boltzmann,
    "ranking": __ranking,
    "tournament": __tournament,
}


# Build a selection method from the given configuration
def get_selection_method(config: dict) -> SelectionMethod:
    # Get selection methods
    selection_method1 = config["method1"]
    if selection_method1 not in __selection_methods:
        raise ValueError(f"Unknown selection method: {selection_method1}")

    selection_method1 = __selection_methods[selection_method1]

    selection_method2 = config["method2"]
    if selection_method2 not in __selection_methods:
        raise ValueError(f"Unknown selection method: {selection_method2}")

    selection_method2 = __selection_methods[selection_method2]

    # Get proportion of population to be selected by method 1
    method1_propotion = config["method1_proportion"]
    if method1_propotion < 0 or method1_propotion > 1:
        raise ValueError(
            f"Method 1 proportion must be between 0 and 1. Received: {method1_propotion}"
        )

    selection_amount = config["amount"]

    # Build the selection method joining the two methods
    def joined_selection_method(
            population: list[Character], fitness_function: FitnessFunction
    ) -> list[Character]:
        amount_1 = int(selection_amount * method1_propotion)

        return selection_method1(
            population[:amount_1], fitness_function, amount_1
        ) + selection_method2(
            population[amount_1:], fitness_function, selection_amount - amount_1
        )

    return joined_selection_method


# --------------------- Helpers --------------------- #

def compare(character1, character2, fitness_function):
    return fitness_function(character1) - fitness_function(character2)

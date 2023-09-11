import copy
from typing import Callable, Dict
from individual.character import Character
from individual.fitness import FitnessFunction
from math import exp
import random


# --------------------- Methods --------------------- #


def __elitism(
    population: list[Character],
    fitness_function: FitnessFunction,
    selection_amount: int,
) -> list[Character]:
    population.sort(key=fitness_function, reverse=True)
    selections = population[:selection_amount]
    return selections


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
    random_init = random.random()
    j = 0
    for _ in range(selection_amount):
        random_value = (random_init + j) / selection_amount - 1
        j += 1

        # Encuentra el individuo correspondiente al valor aleatorio
        selected_individual = None
        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if random_value <= cumulative_probability:
                selected_individual = population[i]
                break

        if selected_individual is not None:
            selections.append(selected_individual)

    return selections


def __boltzmann(
    population: list[Character],
    fitness_function: FitnessFunction,
    selection_amount: int,
    temperature: int,
) -> list[Character]:
    # e^(f(i)/T)
    probabilities = [
        exp(fitness_function(character) / temperature) for character in population
    ]

    # Normalizo las probabilidades -> la sum me da 1
    total_probability = sum(probabilities)
    normalized_probabilities = [p / total_probability for p in probabilities]

    # Hago las selecciones random, teniendo en cuenta los pesos
    selected_population = random.choices(
        population, weights=normalized_probabilities, k=selection_amount
    )

    # retorno la poblacion seleccionada
    return selected_population


def __tournament(
    population: list[Character],
    fitness_function: FitnessFunction,
    selection_amount: int,
    tournament_size: int,
) -> list[Character]:
    selections = []

    for _ in range(selection_amount):
        # Agrupo M, y tomo el maximo. Creo que en el caso de que tengan igual fitness,
        # max() toma el primero que encuentra, no se si eso esta mal.
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=fitness_function)
        selections.append(winner)

    return selections


def __tournament_probabilistic(
    population: list[Character],
    fitness_function: FitnessFunction,
    selection_amount: int,
    tournament_size: int,
    threshold: float,
) -> list[Character]:
    selections = []

    for _ in range(selection_amount):
        random_probability = random.random()
        tournament = random.sample(population, tournament_size)

        if random_probability < threshold:
            selections.append(max(tournament, key=fitness_function))
        else:
            selections.append(min(tournament, key=fitness_function))

    return selections


def __ranking(
    population: list[Character],
    fitness_function: FitnessFunction,
    selection_amount: int,
) -> list[Character]:
    ranked_list = copy.copy(population)

    ranked_list.sort(key=fitness_function, reverse=True)

    size = len(ranked_list)

    # TODO: ver si seria mejor crear un dict character -> ranking
    # para agilizar la obtencion del puesto
    # (no usar index de la ranked_list)

    return __roulette(
        population,
        lambda character: (size - ranked_list.index(character)) / size,
        selection_amount,
    )


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
    selection_amount = config["amount"]

    # Get selection methods
    selection_method1_name = config["method1"]
    selection_method1 = __get_method(selection_method1_name, selection_amount, config)

    selection_method2_name = config["method2"]
    selection_method2 = __get_method(selection_method2_name, selection_amount, config)

    # Get proportion of population to be selected by method 1
    method1_proportion = config["method1_proportion"]
    if method1_proportion < 0 or method1_proportion > 1:
        raise ValueError(
            f"Method 1 proportion must be between 0 and 1. Received: {method1_proportion}"
        )

    # Build the selection method joining the two methods
    def joined_selection_method(
        population: list[Character], fitness_function: FitnessFunction
    ) -> list[Character]:
        amount_1 = int(selection_amount * method1_proportion)

        return selection_method1(
            population, fitness_function, amount_1
        ) + selection_method2(population, fitness_function, selection_amount - amount_1)

    return joined_selection_method


# --------------------- Helpers --------------------- #


def __compare(character1, character2, fitness_function):
    return fitness_function(character1) - fitness_function(character2)


# Returns the selection method with the given name
# It configures the method with the given parameters if needed
def __get_method(
    name: str, selection_amount: int, config: Dict
) -> Callable[[list[Character], FitnessFunction, int], list[Character]]:
    if name not in __selection_methods:
        raise ValueError(f"Unknown selection method: {name}")

    # Special cases
    if name == "boltzmann":
        boltzmann_config = config["boltzmann"]
        temperature = boltzmann_config["temperature"]

        return lambda population, fitness_function, amount: __boltzmann(
            population, fitness_function, selection_amount, temperature
        )
    if name == "tournament":
        tournament_config = config["tournament"]
        tournament_size = tournament_config["size"]

        if tournament_size > selection_amount:
            raise ValueError(
                f"Tournament size ({tournament_size}) must be less than or equal to selection amount ({selection_amount})"
            )

        is_probabilistic = tournament_config["probabilistic"]
        if is_probabilistic:
            threshold = tournament_config["threshold"]

            if threshold < 0 or threshold > 1:
                raise ValueError(
                    f"Tournament threshold must be between 0 and 1. Received: {threshold}"
                )

            return (
                lambda population, fitness_function, amount: __tournament_probabilistic(
                    population,
                    fitness_function,
                    amount,
                    tournament_size,
                    threshold,
                )
            )

        return lambda population, fitness_function, amount: __tournament(
            population, fitness_function, amount, tournament_size
        )

    # No special parameters
    return lambda population, fitness_function, amount: __selection_methods[name](
        population, fitness_function, amount
    )

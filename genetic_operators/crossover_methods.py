import random

CHROMOSOME_LENGTH = 6


def __assignation(from_point, to_point, child1, child2, chromosome1, chromosome2):
    for i in range(from_point, to_point):
        child1[i] = chromosome1[i]
        child2[i] = chromosome2[i]


def anular(point, length, chromosome1, chromosome2):
    child1 = child2 = []

    if point + length > CHROMOSOME_LENGTH:
        excess_length = point + length - CHROMOSOME_LENGTH
        __assignation(0, excess_length, child2, child1, chromosome1, chromosome2)
        __assignation(excess_length, point, child1, child2, chromosome1, chromosome2)
        __assignation(point, CHROMOSOME_LENGTH, child2, child1, chromosome1, chromosome2)
    else:
        __assignation(0, point, child1, child2, chromosome1, chromosome2)
        __assignation(point, point + length, child2, child1, chromosome1, chromosome2)
        __assignation(point + length, CHROMOSOME_LENGTH, child1, child2, chromosome1, chromosome2)

    return child1, child2


def point(point, chromosome1, chromosome2):
    child1 = child2 = []

    __assignation(0, point, child1, child2, chromosome1, chromosome2)
    __assignation(point, CHROMOSOME_LENGTH, child2, child1, chromosome1, chromosome2)

    return child1, child2


def two_point(point1, point2, chromosome1, chromosome2):
    child1 = child2 = []

    __assignation(0, point1, child1, child2, chromosome1, chromosome2)
    __assignation(point1, point2, child2, child1, chromosome1, chromosome2)
    __assignation(point2, CHROMOSOME_LENGTH, child1, child2, chromosome1, chromosome2)

    return child1, child2


def uniform(probability, chromosome1, chromosome2):
    child1 = child2 = []

    for i in range(CHROMOSOME_LENGTH):
        if random.random() < probability:
            child2[i] = chromosome1[i]
            child1[i] = chromosome2[i]
        else:
            child1[i] = chromosome1[i]
            child2[i] = chromosome2[i]

    return child1, child2

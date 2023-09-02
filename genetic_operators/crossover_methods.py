CHROMOSOME_LENGTH = 6


def __direct_assignation(from_point, to_point, child1, child2, chromosome1, chromosome2):
    for i in range(from_point, to_point + 1):
        child1[i] = chromosome1[i]
        child2[i] = chromosome2[i]


def __inverse_assignation(from_point, to_point, child1, child2, chromosome1, chromosome2):
    for i in range(from_point, to_point + 1):
        child2[i] = chromosome1[i]
        child1[i] = chromosome2[i]

def anular():
    pass


def point(point, chromosome1, chromosome2):
    child1 = child2 = []

    __direct_assignation(0, point, child1, child2, chromosome1, chromosome2)
    __inverse_assignation(point + 1, CHROMOSOME_LENGTH, child1, child2, chromosome1, chromosome2)

    return child1, child2


def two_point(point1, point2, chromosome1, chromosome2):
    pass


def uniform():
    pass

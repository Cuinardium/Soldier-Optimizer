CHROMOSOME_LENGTH = 6


def anular():
    pass


def point(point, chromosome1, chromosome2):
    child1 = child2 = []
    for i in range(point):
        child1[i] = chromosome1[i]
        child2[i] = chromosome2[i]

    for i in range(point + 1, CHROMOSOME_LENGTH + 1):
        child2[i] = chromosome1[i]
        child1[i] = chromosome2[i]

    return child1, child2


def two_point():
    pass


def uniform():
    pass

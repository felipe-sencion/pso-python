class Sphere:
    MIN_VALUE = -5.12
    MAX_VALUE = 5.12
    def __init__(self):
        pass
    def fitness(self, vector):
        z = 0
        for dimension in vector:
            z += dimension**2
        return z

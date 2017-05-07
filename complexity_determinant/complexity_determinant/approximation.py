import math
from numpy import array, dot, transpose
from numpy.linalg import inv
from complexity import Complexity
from logger import Logger, LoggingLevel


class Approximation:
    """Object containing informations about the complexity"""
    def __init__(self, base, measurements):
        self.measurements = measurements
        self.base = base
        self.factors = self.__calculate_factors()

    def __calculate_factors(self):
        """Wraps __factors_vector for easy usage"""
        multiplier = []
        values = []
        # Fill multiplier and values
        for x, y in self.measurements:
            row = []
            values.append([y]) # [[1],[2],[3]] (1xN)
            for f in self.base:
                row.append(f(x))
            multiplier.append(row)

        # Transform lists to arrays
        multiplier = array(multiplier)
        values = array(values)

        # Calculate factors
        return self.__factors_vector(multiplier, values)

    @staticmethod
    def __factors_vector(A, b):
        """
            Calculates factors vector from given matrices
            factors = (At*A)^(-1) x At x b
            <=>
            factors = Bi x At x b where
                Bi = (At*A)^(-1)
        """
        At = transpose(A)
        B = dot(At, A)
        Bi = inv(B)
        return dot(dot(Bi, At), b)

    def __call__(self, x):
        """Returns approximation value for given x"""
        value = 0
        for i in range(len(self.base)):
            fun = self.base[i]
            factor = self.factors[i][0]
            value += factor*fun(x)
        return value

    @property
    def mean_squared_error(self):
        """
            Returns mean squared error
            https://en.wikipedia.org/wiki/Mean_squared_error
        """
        error = 0
        for x, y in self.measurements:
            error += (y-self(x))**2
        return error/len(self.measurements)
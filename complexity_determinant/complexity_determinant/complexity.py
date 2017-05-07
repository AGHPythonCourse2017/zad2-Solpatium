"""Complexity class and function choosing the best complexity based on measures"""
import math
from enum import Enum
from scipy.optimize import newton
from approximation import Approximation
from logger import Logger, LoggingLevel

class ComplexityLevel(Enum):
    """Available complexities"""
    N = "O(n)"
    NLOGN = "O(nlog(n))"
    N2 = "O(n^2)"
    def __str__(self):
        return self.value

class Complexity:
    """Object containing informations about the complexity"""
    __BASES = {
        ComplexityLevel.N: [
            lambda x: 1,
            lambda x: x,
        ],
        ComplexityLevel.N2: [
            lambda x: 1,
            lambda x: x,
            lambda x: x*x
        ],
        ComplexityLevel.NLOGN: [
            lambda x: 1,
            lambda x: math.log(x),
            lambda x: x,
            lambda x: x*math.log(x)
        ]
    }

    def __init__(self, complexity_level, measurements):
        self.complexity_level = complexity_level
        self.approximation = Approximation(self.__BASES[complexity_level], measurements)

    def complexity_info(self):
        """Returns most basic info about the complexity"""
        return self.__str__()

    def execution_time(self, problem_size):
        """Returns estimated execution time for problem of given size"""
        return self.approximation(problem_size)

    def max_problem_size_for_time(self, time):
        """Returns max problem size for given time"""
        function = lambda x: self.approximation(x)-time
        return newton(function, 5, maxiter=200)

    def is_valid(self):
        """Returns information if approximation is ok. Quadratic function might become a linear"""
        if self.complexity_info == ComplexityLevel.N:
            # No distortion in this case
            return True
        else:
            epsilon = 10e-3
            # If the most important factor is not significant at all there is something wrong
            return self.approximation.factors[-1][-1] > epsilon

    def __str__(self):
        # Get the most important factor
        key_factor = self.approximation.factors[-1][-1]
        modifier = ''
        if key_factor < 0.5:
            modifier = ' better than'
        if key_factor > 5:
            modifier = ' worse than'
        return 'Complexity{} {}. Mean squared error={}'.format(
            modifier,
            self.complexity_level,
            self.approximation.mean_squared_error
        )

def best_complexity(measurements):
    """Returns the best complexity based on measurements"""
    # Check measurements
    if len(measurements) < 4:
        Logger.log("At least 4 measurements are required", LoggingLevel.ERR)
        return None

    proposed = [
        Complexity(ComplexityLevel.NLOGN, measurements),
        Complexity(ComplexityLevel.N, measurements),
        Complexity(ComplexityLevel.N2, measurements)
    ]

    def filter_invalid(complexity):
        """Leavs only valid complexities"""
        if not complexity.is_valid():
            Logger.log('Invalid {}'.format(complexity), LoggingLevel.DEBUG)
            return False
        return True

    possible = filter(filter_invalid, proposed)
    chosen = min(possible, key=lambda x: x.approximation.mean_squared_error)

    Logger.log('From {} the best is {}'.format(possible, chosen), LoggingLevel.DEBUG)

    return chosen

"""Complexity class and function choosing the best complexity based on measures"""
import math
import timeout_decorator
from enum import Enum
from scipy.optimize import newton
from .approximation import Approximation
from .logger import Logger, LoggingLevel
from .timeout import timeout, TimeoutExceeded
from .timer import Timer
from .files_importer import properties_from_files

class ComplexityLevel(Enum):
    """Available complexities"""
    N = "O(n)"
    NLOGN = "O(nlog(n))"
    N2 = "O(n^2)"
    def __str__(self):
        return self.value

    @staticmethod
    def bases():
        """Returns bases for complexities"""
        return {
            ComplexityLevel.N: [
                lambda x: 1,
                lambda x: x,
            ],
            ComplexityLevel.N2: [
                lambda x: 1,
                # lambda x: x,
                lambda x: x*x
            ],
            ComplexityLevel.NLOGN: [
                lambda x: 1,
                # lambda x: math.log(x),
                # lambda x: x,
                lambda x: x*math.log(x)
            ]
        }

class Complexity:
    """Object containing informations about the complexity"""
    def __init__(self, complexity_level, measurements):
        self.complexity_level = complexity_level
        self.approximation = Approximation(ComplexityLevel.bases()[complexity_level], measurements)

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
        """
            Returns information if approximation is ok.
            Quadratic and logarithmic functions might become a linear
        """
        if self.complexity_level == ComplexityLevel.N:
            # No distortion in this case
            return True
        else:
            epsilon = 10e-10
            # If the most important factor is not significant at all there is something wrong
            return self.approximation.factors[-1][-1] > epsilon

    def __str__(self):
        # Get the most important factor
        key_factor = self.approximation.factors[-1][-1]
        modifier = ''
        if key_factor < 0.05:
            modifier = ' better than'
        if key_factor > 10:
            modifier = ' worse than'
        return 'Complexity{} {}. Mean squared error={}'.format(
            modifier,
            self.complexity_level,
            self.approximation.mean_squared_error
        )

def determine(structure, test, clean_function, max_execution=30):
    """Measures execution times and returns complexity object"""
    class TestedFunctionError(Exception):
        """Exception thrown when tested function throws an exception"""
        pass

    def execute_function(problem):
        """Executes tested function and returns execution time"""
        try:
            timer = Timer()
            timer.start()
            test(problem)
            timer.stop()
            return timer.time
        except TimeoutExceeded as exceded:
            # We might catch this exception accidently
            raise exceded
        except Exception as e:
            Logger.log(str(e), LoggingLevel.ERR)
            raise TestedFunctionError

    @timeout(max_execution)
    def measure_time(measurements):
        """Executes tested function for all problems"""
        for size, problem in structure.items():
            try:
                measurements[size] = execute_function(problem)
            except TestedFunctionError:
                Logger.log("Raised exception for problem size {}.".format(size), LoggingLevel.ERR)

    try:
        measurements = {}
        measure_time(measurements)
    except TimeoutExceeded:
        message = "Exceeded {}s for all problems".format(max_execution)
        Logger.log(message, LoggingLevel.WARN)

    clean_function()

    measurements = list(measurements.items()) # List of tuples
    return best_complexity(measurements)

def determine_from_files(structure, test, clean, timeout=30):
    """Wrapper around determine, reads all needed data from files"""
    imported = properties_from_files(structure, test, clean)
    if imported is None:
        Logger.log("Structure or functions don't exist", LoggingLevel.ERR)
        return None
    return determine(imported[0], imported[1], imported[2], timeout)

def best_complexity(measurements):
    """Returns the best complexity based on measurements"""
    # Check measurements
    if len(measurements) < 2:
        Logger.log("At least 2 measurements are required", LoggingLevel.ERR)
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

    possible = [x for x in proposed if filter_invalid(x)]
    chosen = min(possible, key=lambda x: x.approximation.mean_squared_error)

    Logger.log('The best is {}'.format(chosen), LoggingLevel.DEBUG)

    return chosen

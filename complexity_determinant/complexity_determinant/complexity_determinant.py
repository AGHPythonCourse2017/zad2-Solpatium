from timeout_decorator import timeout, TimeoutExceeded
from logger import Logger, LoggingLevel
from timer import Timer
from complexity import best_complexity
import importlib

class TestedFunctionError(Exception):
    """Exception thrown when tested function throws an exception"""
    pass

class ComplexityDeterminant:
    TOTAL_TIMEOUT = 30
    SINGLE_TIMEOUT = 10

    """Determines algorithm's complexity in the big O notation"""
    def __init__(self, structures_map, tested_function, clean_up_function):
        self.structures_map = structures_map
        self.tested_function = tested_function
        self.clean_up_function = clean_up_function
        self.measurements = {}

    @timeout(SINGLE_TIMEOUT)
    def __execute_function(self, problem):
        """Executes tested function and returns execution time"""
        try:
            timer = Timer()
            timer.start()
            self.tested_function(problem)
            timer.stop()
            return timer.time
        except:
            raise TestedFunctionError

    @timeout(TOTAL_TIMEOUT)
    def __measure_time(self):
        """Executes tested function for all problems"""
        for size, problem in self.structures_map.items():
            try:
                self.measurements[size] = self.__execute_function(problem)
            except TestedFunctionError:
                Logger.log("Raised exception for problem size {}.".format(size), LoggingLevel.ERR)
                self.measurements = {}
            except TimeoutExceeded:
                message = "Exceeded {}s for problem size {}".format(self.SINGLE_TIMEOUT, size)
                Logger.log(message, LoggingLevel.WARN)

    @property
    def complexity(self):
        """Returns complexity object"""
        self.__measure_time()
        try:
            measurements = list(self.measurements.items()) # List of tuples
        except TimeoutExceeded:
            message = "Exceeded {}s for all problems".format(self.TOTAL_TIMEOUT)
            Logger.log(message, LoggingLevel.WARN)

        self.clean_up_function()

        return best_complexity(measurements)

    @staticmethod
    def from_files(structure_file, tested_file, clean_file):
        """Creates a complexity determinant object from files"""
        results = tested_properties_from_files(structure_file, tested_file, clean_file)
        if results is None:
            Logger.log("Structure or functions doesn't exist", LoggingLevel.ERR)
            return None
        else:
            complexity = ComplexityDeterminant(results[0], results[1], results[2])
            return complexity

def tested_properties_from_files(structure_file, tested_file, clean_file):
    """Returns tuple with values to be tested"""
    def module_name(file_name):
        """Removes .py from file name"""
        return file_name.replace(".py", "")

    # Get modules' names
    structure_file = module_name(structure_file)
    tested_file = module_name(tested_file)
    clean_file = module_name(clean_file)

    try:
        # Data structure
        structure_module = importlib.import_module(structure_file)
        structure = structure_module.data_structure

        # Function or class function
        function_module = importlib.import_module(tested_file)
        function = None
        if 'tested_function' in dir(function_module):
            # Just a function
            function = function_module.tested_function
        else:
            # Static function in a class
            for attr in dir(function_module):
                prop = getattr(function_module, attr)
                if hasattr(prop, 'tested_function'):
                    function = prop.tested_function
                    break

        if function is None:
            return None

        # Clean function
        clean_module = importlib.import_module(clean_file)
        clean = clean_module.clean_function

        return (structure, function, clean)
    except AttributeError:
        return None
    except SyntaxError as syntax:
        Logger.log("One files has an invalid syntax: {}".format(str(syntax)), LoggingLevel.ERR)
        return None
    except ModuleNotFoundError as not_found:
        Logger.log("One of files doesn't exist: {}".format(str(not_found)), LoggingLevel.ERR)
        return None

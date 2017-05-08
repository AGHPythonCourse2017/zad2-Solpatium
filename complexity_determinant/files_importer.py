import importlib
from .logger import Logger, LoggingLevel


def properties_from_files(structure_file, tested_file, clean_file):
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
    except AttributeError as attribute:
        Logger.log("Missing test property: {}".format(str(attribute)),
                   LoggingLevel.ERR)
        return None
    except SyntaxError as syntax:
        Logger.log("One files has an invalid syntax: {}".format(str(syntax)),
                   LoggingLevel.ERR)
        return None
    except ModuleNotFoundError as not_found:
        Logger.log("One of files doesn't exist: {}".format(str(not_found)),
                   LoggingLevel.ERR)
        return None

"""Logger parts used by complexity determinant"""
from enum import Enum
import sys

class LoggingLevel(Enum):
    """Logging levels for logger"""
    DEBUG = 1
    WARN = 2
    ERR = 3
    def __lt__(self, other):
        """Comparator"""
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class LoggingOutput(Enum):
    """Enum used to set logger's output"""
    FILE = 0
    STDOUT = 1
    STDERR = 2
    NONE = 3

class Logger:
    """Simple logger"""
    logging_output = LoggingOutput.STDOUT
    logging_file = "./log.txt"
    minimum_log_level = LoggingLevel.DEBUG

    @classmethod
    def log(cls, what, level=LoggingLevel.DEBUG):
        """Logs given string"""
        if cls.minimum_log_level > level:
            return
        cls.__write(what)

    @classmethod
    def __write(cls, what):
        {
            LoggingOutput.STDOUT: lambda: print(what),
            LoggingOutput.STDERR: lambda: print(what, file=sys.stderr),
            LoggingOutput.NONE: lambda: None,
            LoggingOutput.FILE: lambda: cls.__write_to_file(what)
        }[cls.logging_output]()

    @classmethod
    def __write_to_file(cls, what):
        with open(cls.logging_file, "a") as file:
            file.write(what)




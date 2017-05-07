"""Timer for getting execution time"""
from time import process_time

class Timer:
    """Simple timer"""
    def __init__(self):
        self.__beg = self.__end = 0
    def start(self):
        """Starts timer"""
        self.__beg = process_time()
    def stop(self):
        """Ends timer"""
        self.__end = process_time()
    @property
    def time(self):
        """Returns time measured"""
        return self.__end-self.__beg

from datetime import date, datetime
from functools import total_ordering
from enum import Enum
from importlib.metadata import files
import logging

@total_ordering
class DbgStmtLevel(Enum):
    NONE = 0
    STMTS = 1
    DATAFILL = 2

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
            
        return NotImplemented

class SQPLogger():
    def __init__(self, logger : logging.Logger, dbdbglevel : DbgStmtLevel):
        self._logger = logger
        self._dbloglevel = dbdbglevel

    def log_stmt(self, formatstr : str, *args):
        if self._dbloglevel >= DbgStmtLevel.STMTS:
            self._logline("ST " + formatstr, *args)

    def log_dtafill(self, formatstr : str, *args):
        if self._dbloglevel >= DbgStmtLevel.DATAFILL:
            self._logline("DF " + formatstr, *args)


    def _logline(self, fs, *args):
        logstr = fs.format(*args) 
        self._logger.debug(logstr)

    
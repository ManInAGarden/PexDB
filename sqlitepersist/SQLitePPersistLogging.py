from datetime import date, datetime
from functools import total_ordering
from enum import Enum

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
    def __init__(self, filepath : str, dbglevel : DbgStmtLevel):
        self._logfilepath = filepath
        self._level = dbglevel
        self._logcache = None

    def log_stmt(self, formatstr : str, *args):
        if self._level >= DbgStmtLevel.STMTS:
            self._logline("ST " + formatstr + "\n", *args)

    def log_dtafill(self, formatstr : str, *args):
        if self._level >= DbgStmtLevel.DATAFILL:
            self._logline("DF " + formatstr + "\n", *args)


    def _logline(self, fs, *args):
        dts = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        logstr = dts + " " + fs.format(*args) 

        try:
            with open(self._logfilepath, "a") as f:
                if self._logcache is not None:
                    for logs in self._logcache:
                        f.write(logs)
                    self._logcache = None

                f.write(logstr)
        except Exception as ex:
            self._add_to_loggcache(logstr)

    def _add_to_loggcache(self, ls):
        if self._logcache is None:
            self._logcache = []

        self._logcache.append(ls + " _DELAYED_")

    
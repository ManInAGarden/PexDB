
from subprocess import Popen, PIPE
from subprocess import check_output
from platform import system

class ExtOpener:
    MYOSNAME = system().lower()

    def __init__(self, fname : str):
        self._ftoopen = fname

    def get_command(self):
        if 'windows' in ExtOpener.MYOSNAME:
            opener = 'start'
        elif 'osx' in ExtOpener.MYOSNAME or 'darwin' in ExtOpener.MYOSNAME:
            opener = 'open'
        else:
            opener = 'xdg-open'
        
        return "{} {}".format(opener, self._ftoopen)

    def open(self, showshell=False):
        subproc = Popen(
            self.get_command(),
            stdout=PIPE, stderr=PIPE, shell=showshell
        )
        subproc.wait()
        return subproc
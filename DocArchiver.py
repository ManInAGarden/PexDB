from os import *

class DocArchiver:
    """class for handling archivation of documents in a filestore aka directory"""

    SUBPRAE = "SUB_"
    
    def __init__(self, dirpath : str):
        """init class with a given directory path"""
        if dirpath is None:
            raise Exception("Dirpath must not be None")

        self._basepath = dirpath

    def subname(self, num : int):
        return "{}{:03d}".format(DocArchiver.SUBPRAE, num)

    def prepare_archive(self, dirnum: int = 10):
        """prepare an empty archive"""
        if not path.exists(self._basepath):
            makedirs(self._basepath)

        for i in range(dirnum):
            mkdir(self._basepath + "/" + self.subname(i))
        
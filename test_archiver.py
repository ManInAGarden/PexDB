from genericpath import isdir, isfile
import unittest
from os import *
import pathlib as pl
from PersistClasses import *
from DocArchiver import *

class TestArchiver(unittest.TestCase):

    _bpath = "./archivertest"
    _dirnum = 5

    def test_archive_creation(self):
        """Test the creation of a new archive"""

        archi = DocArchiver(TestArchiver._bpath)
        archi.prepare_archive(TestArchiver._dirnum) #prepare with 5 subarchives

        #now check if everything has been created as expected
        assert path.isdir(TestArchiver._bpath)
        for i in range(DocArchiver._dirnum):
            subp = TestArchiver._bpath + "/" + DocArchiver.SUBPRAE + "{:03d}".format(i)
            assert path.isdir(subp)

    def doCleanups(self) -> None:
        self.removecontents(TestArchiver._bpath)
        
    
    def removecontents(self, pname):
        if not path.exists(pname):
            return

        fds = listdir(pname)
        for fd in fds:
            fullfd = pname + "/" + fd
            if isfile(fullfd):
                if pl.Path(fullfd).suffix != ".zip":
                    raise Exception("Something very wrong. Non-zip file encountered in removecontents of DocArchive")

                remove(fullfd)
            elif isdir(fullfd):
                self.removecontents(fullfd)
            else:
                raise Exception("Strange object named <{}> found in directory <{}>".format(fd, pname))

        remove(pname) #also remove topdir
            


if __name__ == '__main__':
    unittest.main()
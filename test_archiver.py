from genericpath import isdir, isfile
import unittest
from os import *
import pathlib as pl
from PersistClasses import *
from DocArchiver import *

class TestArchiver(unittest.TestCase):

    _bpath = "./archivertest"
    _dirnum = 5

    def setUp(self) -> None:
        self._cleanups = []
        DocArchiver.prepare_archive(TestArchiver._bpath, TestArchiver._dirnum)
        self._cleanups.append(TestArchiver._bpath)

    def test_archive_creation(self):
        """Test the creation of a new archive"""

        spec_bpath = "./specarchivertest"
        spec_dirnum = 3
        DocArchiver.prepare_archive(spec_bpath, spec_dirnum)
        self._cleanups.append(spec_bpath)

        #now check if everything has been created as expected
        assert path.isdir(spec_bpath)
        for i in range(spec_dirnum):
            subp = spec_bpath + "/" + DocArchiver.SUBPRAE + "{:03d}".format(i)
            assert path.isdir(subp)


    def test_simple_archiving(self):
        archi = DocArchiver(self._bpath)

        assert archi is not None

        archname, fext = archi.archive_file("./testfiles/QXP_HTAM_Filamentum_ABS_100_0_0001.jpg")
        assert archname is not None
        assert fext == ".jpg"
        assert path.exists(archname)

    def doCleanups(self) -> None:
        for bp in self._cleanups:
            self.removecontents(bp)
        
    
    def removecontents(self, pname):
        if not path.exists(pname):
            return

        fds = listdir(pname)
        for fd in fds:
            fullfd = pname + "/" + fd
            if path.isfile(fullfd):
                if pl.Path(fullfd).suffix != ".zip":
                    raise Exception("Something very wrong. Non-zip file encountered in removecontents of DocArchive")

                remove(fullfd) #remove file
            elif path.isdir(fullfd):
                self.removecontents(fullfd)
            else:
                raise Exception("Strange object named <{}> found in directory <{}>".format(fd, pname))

        rmdir(pname) #also remove topdir
            


if __name__ == '__main__':
    unittest.main()
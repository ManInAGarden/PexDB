from os import *
import pathlib as pl
import random as rn
import uuid
import zipfile as zf


class DocArchiver:
    """class for handling archivation of documents in a filestore aka directory"""

    SUBPRAE = "SUB_"
    
    def __init__(self, dirpath : str):
        """init class with a given directory path"""
        if dirpath is None:
            raise Exception("Dirpath must not be None")

        self._basepath = dirpath
        self._check_archive()

    def _check_archive(self):
        subdirs = listdir(self._basepath)
        
        ct = 0
        for fd in subdirs:
            fulldname = self._basepath + "/" + fd
            if self.is_archdir(fulldname):
                ct += 1

        self._numdirs = ct

    def is_archdir(self, fname):
        if path.isfile(fname):
            return False
        
        if path.isdir(fname):
            parts = fname.split("_")
            if not len(parts) == 2:
                return False

            if not parts[0].endswith(DocArchiver.SUBPRAE[0:-1]):
                return False

            nus = parts[1]
            if not len(nus)==3:
                return False
            if not nus.isdigit():
                return False

            return True
        else:
            return False

    #type alias for return value
    ArchiveReturn = tuple[str, str]

    def archive_file(self, fpath) -> ArchiveReturn:
        """archive a single file
        fpath: full path to the file

        returns: name of the archive file and extension of the archived file
        """
        if not path.isfile(fpath):
            raise Exception("Given path <{}> does not point to a file".format(fpath))


        extname = pl.Path(fpath).suffix
        if extname is None or len(extname)==0:
            raise Exception("Only files with a non zero length extension can be archived")

        if extname==".":
            raise Exception("Only files with a non zero length extension can be archived")


        dirn = rn.randint(0, self._numdirs-1)
        dirname = self._basepath + "/" + self._subname(dirn)

        archname = uuid.uuid4().hex + ".zip"
        fullarchname = dirname + "/" + archname
        aname = path.basename(fpath)
        with zf.ZipFile(fullarchname, 'x', zf.ZIP_DEFLATED) as zip_f:
            zip_f.write(fpath, arcname=aname)

        return fullarchname, extname

       

        

    @classmethod
    def _subname(self, num : int):
        return "{}{:03d}".format(DocArchiver.SUBPRAE, num)

    @classmethod
    def prepare_archive(cls, basepath : str, dirnum: int = 10):
        """prepare an empty archive"""
        if not path.exists(basepath):
            makedirs(basepath)

        for i in range(dirnum):
            subpath = basepath + "/" + cls._subname(i)
            if not path.exists(subpath):
                mkdir(subpath)
        
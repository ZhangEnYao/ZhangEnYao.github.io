import os
import pathlib
import shutil

from .configuration import CATCH, SCRIPTS, MATHEMATICS, TEMPORARY



class Manager:

    def clear(self):

        for root, directories, files in pathlib.Path('.').walk():
            for file in files:
                file = pathlib.Path.joinpath(root, file)
                if file.stem.startswith(MATHEMATICS) and file.suffix not in (".tex", ".pdf"):
                    os.remove(file)
        
        if (path := pathlib.Path(TEMPORARY)).exists():
            shutil.rmtree(path)

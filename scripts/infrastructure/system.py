import dataclasses
import pathlib



class Path(pathlib.Path):
    def __new__(cls, *paths):
        return pathlib.Path.joinpath(*(path if isinstance(path, pathlib.Path) else pathlib.Path(str(path)) for path in paths))


@dataclasses.dataclass
class File:
    file: pathlib.Path

    @property
    def create_time(self):
        return self.file.stat().st_birthtime
    
    def __str__(self):
        return str(self.file.with_suffix(''))

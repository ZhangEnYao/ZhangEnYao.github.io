import dataclasses
import enum
import pathlib



class HEADER(enum.Enum):
    DOCUMENT = 0
    PART = enum.auto()
    CHAPTER = enum.auto()
    SECTION = enum.auto()
    SUBSECTION = enum.auto()
    SUBSUBSECTION = enum.auto()
    PARAGRAPH = enum.auto()
    SUBPARAGRAPH = enum.auto()

class Header:
    def __new__(cls, level):
        return HEADER(level).name.lower()
    
@dataclasses.dataclass
class Title:
    root: pathlib.Path

    @property
    def level(self):
        return len(self.root.parts) - 1
    
    @property
    def indent(self):
        return '\t' * self.level

    @property
    def header(self):
        return Header(level=self.level)
    
    @property
    def description(self):
        return Description(description=self.root.stem)

class Description:
    def __new__(cls, description: str):
        return description.replace('_', ' ').capitalize()

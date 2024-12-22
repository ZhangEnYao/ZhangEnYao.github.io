import re
import typing



class Flag:

    PATTERN=r"(^[a-z]|(?<=_)[a-z])"

    def __init__(self, name: str):
        self.name = name

    @property
    def short(self):
        initialism = re.findall(pattern=self.PATTERN, string=self.name)
        abbreviation = ''.join(initialism)
        short = f"-{abbreviation}"
        return short

    @property
    def long(self):
        long = f"--{self.name}"
        return long

class Argument:

    def __new__(self, *arguments:tuple, **keyword_arguments:dict[str, typing.Any]) -> dict:
        return keyword_arguments

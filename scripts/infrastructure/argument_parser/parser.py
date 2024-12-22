import argparse
import dataclasses
import typing

from .domain import Arguments
from .arguments import Flag



class Parser:

    def __init__(self, structure: typing.Type[dataclasses.dataclass]):
        self.structure = structure
        self.parser = argparse.ArgumentParser()
    
    def parse(self, argument_vector:tuple[str]=None) -> dict:
        for field in dataclasses.fields(class_or_instance=self.structure):
            flag = Flag(name=field.name)
            self.parser.add_argument(
                flag.short,
                flag.long,
                type=field.type,
                **field.default_factory
            )
        
        arguments = self.parser.parse_args(argument_vector)
        arguments = self.structure(**arguments.__dict__)

        return arguments

class ArgumentParser:

    def __init__(self):
        self.parser = Parser(structure=Arguments)

    def parse(self, argument_vector:tuple[str]=None) -> Arguments:
        arguments = self.parser.parse(argument_vector)
        return arguments

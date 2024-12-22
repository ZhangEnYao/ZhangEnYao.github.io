import argparse
import operator
import pprint


from scripts.infrastructure.argument_parser.parser import ArgumentParser
from scripts.build.build import Builder
from scripts.differentiate import Differentiate
from scripts.infrastructure.version_control import VersionControl
from scripts.clear import Manager
from scripts.structure.structure import Generator, Graphs



class Script:
    @staticmethod
    def version_control(*arguments, **keyword_arguments):
        VersionControl.version_control()

    @staticmethod
    def build(*arguments, **keyword_arguments):
        Builder().generate()

    @staticmethod
    def clear(*arguments, **keyword_arguments):
        Manager().clear()
    
    @staticmethod
    def differentiate(*arguments, **keyword_arguments):
        VersionControl.differentiate()
        Differentiate().differentiate()

    @staticmethod
    def query(nodes: set):
        pprint.pprint(Graphs(generator=Generator()).query(nodes), width=130)

arguments = ArgumentParser().parse()
operator.methodcaller(arguments.script, set(arguments.arguments) if arguments.arguments else None)(Script)

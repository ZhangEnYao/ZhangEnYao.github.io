import functools
import pathlib
import typing
import re

from ..infrastructure.formatter import format
from .domain import similarity, Graph, Reference, Nodes, Edge, Response
from ..configuration import DOCUMENT, PATTERN
from ..infrastructure.system import File



class Generator:
    def parse(self, document: File) -> typing.Generator[Graph, Graph, Graph]:
        with open(document.file, "r") as file:
            for index, line in enumerate(file.readlines(), start=1):
                if not (domains := re.findall(pattern=PATTERN.DOMAIN, string=line)):
                    continue

                description = format(line)
                reference = Reference(document.file, index)

                nodes = Nodes(str(domain).capitalize() for domain in domains)
                edge = Edge(reference=reference ,description=description)

                graph = Graph(nodes=nodes, edge=edge)

                yield graph

    def filter(self, directory: pathlib.Path) -> bool:
        if not directory.is_dir():
            return False
        if directory.stem.startswith('.'):
            return False
        if not directory.stem in {DOCUMENT}:
            return False
        return True

    def generate(self) -> typing.Generator[Graph, Graph, Graph]:
        root = pathlib.Path('.')

        for directory in (directory for directory in root.iterdir() if self.filter(directory)):
            for parent, directories, files in directory.walk():
                for document in (File(pathlib.Path.joinpath(parent, file)) for file in files):
                    yield from self.parse(document)

class Graphs:
    def __init__(self, generator: Generator):
        self.generator = generator
    
    @functools.cached_property
    def graphs(self) -> tuple[Graph]:
        return tuple(self.generator.generate())

    def query(self, nodes: set[str], threshold: float = 1) -> tuple[Graph]:
        if nodes:
            nodes = set(node.capitalize() for node in nodes)
            graphs = tuple(graph for graph in self.graphs if similarity(nodes, graph.nodes) >= threshold)
        else:
            graphs = tuple(graph for graph in self.graphs)
        
        response = Response(graphs=graphs)
        
        return response.wrap()

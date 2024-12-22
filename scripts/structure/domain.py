import collections
import collections.abc
import dataclasses
import functools
import inspect
import pathlib

from ..configuration import NETWORK, TEMPORARY
from ..infrastructure.system import Path
from ..infrastructure.formatter import format, to_markdown, to_json



PATTERN = r"\\Domain{([^}]+?)}"

def similarity(operand: set, argument: set) -> float:
    return len(operand.intersection(argument))/len(operand)

class Nodes(collections.Counter):
    pass

@dataclasses.dataclass(unsafe_hash=True)
class Reference:
    file: str
    line: int

@dataclasses.dataclass(unsafe_hash=True)
class Edge:
    reference: Reference
    description: str

@dataclasses.dataclass
class Graph:
    nodes: Nodes
    edge: Edge

@dataclasses.dataclass
class Response:
    graphs: tuple[Graph]

    @functools.cached_property
    def nodes(self) -> tuple[Nodes]:
        return tuple(graph.nodes for graph in self.graphs)

    @functools.cached_property
    def neighbors(self) -> Nodes:
        return functools.reduce(lambda operand, argument: operand + argument, self.nodes) if self.nodes else self.nodes
    
    @property
    def edges(self) -> tuple[Edge]:
        return tuple(graph.edge for graph in self.graphs)
    
    @property
    def relation(self) -> collections.defaultdict:
        relation = collections.defaultdict(set)
        for graph in self.graphs:
            for node in graph.nodes:
                relation[node].add(graph.edge)
        return relation
    
    def wrap(self):
        graphs = {
            name: getattr(self, name)
            for name, member in inspect.getmembers(type(self))
            if isinstance(member, property)
        }
        
        network =  format(graphs) 
        
        Path(TEMPORARY).mkdir(exist_ok=True)
        with open(Path(TEMPORARY, f"{NETWORK}.json"), "w") as file:
            file.write(to_json(network))
        with open(Path(TEMPORARY, f"{NETWORK}.markdown"), "w") as file:
            file.write(to_markdown(network))

        return network

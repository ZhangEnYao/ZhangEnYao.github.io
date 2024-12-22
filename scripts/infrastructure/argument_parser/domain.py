import dataclasses
import enum

from .arguments import Argument



class MetaTokenizer(enum.EnumMeta):

    def __call__(cls, key: str):
        if not cls.__members__:
            raise ValueError(f"{cls.__name__} has no members.")
        
        members = cls.__members__
        default = next(iter(cls))
        
        return members.get(key, default)

class Tokenizer(enum.Enum, metaclass=MetaTokenizer):
    pass


@dataclasses.dataclass
class Arguments:
    script: str = dataclasses.field(default_factory=Argument(default=''))
    arguments: str = dataclasses.field(default_factory=Argument(nargs='*'))

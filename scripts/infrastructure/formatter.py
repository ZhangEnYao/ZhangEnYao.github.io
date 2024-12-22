import collections
import collections.abc
import dataclasses
import json
import re
import typing

from ..configuration import PATTERN



def zero_dimension(object: typing.Type[object]):
    return str(object)

def one_dimension(iterable: collections.abc.Iterable):
    return tuple(format(object) for object in iterable)

def two_dimension(mapping: collections.abc.Mapping):
    return {key: format(value) for key, value in mapping.items()}

def format(root: typing.Type[object]):
    if isinstance(root, str):
        return re.sub(pattern=PATTERN.DOMAIN, repl=r"**\1**", string=root).strip()

    if dataclasses.is_dataclass(root):
        return two_dimension(dataclasses.asdict(root))
    elif isinstance(root, collections.abc.Mapping):
        return two_dimension(root)
    elif isinstance(root, collections.abc.Iterable):
        return one_dimension(root)
    else:
        return zero_dimension(root)

def to_json(root: object):
    return json.dumps(root, indent=4)

def to_markdown(root: object, depth: int=1):
    markdown = ''
    
    if isinstance(root, dict):
        for key, value in root.items():
            markdown = markdown + f"{'#'*depth} {key}\n"
            markdown = markdown + to_markdown(value, depth+1)
    elif isinstance(root, tuple):
        for item in root:
            markdown = markdown + f"{to_markdown(item, depth+1)}\n"
    else:
        markdown = markdown + f"{root}\n"

    return markdown

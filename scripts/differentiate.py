import re
import collections

from .configuration import DIFFERENCES, TEMPORARY, ADDITION, SUBTRACTION
from .infrastructure.system import Path
from .infrastructure.formatter import format, to_json, to_markdown



PATTERN = r"^[\-\+](\s+?(.+))"

class Differentiate:
    def filter(self, file: Path):
        if file.name in (ADDITION, SUBTRACTION):
            return True

    def generator(self):
        files = (file for file in Path(TEMPORARY).iterdir() if self.filter(file))

        for file in files:
            with open(file, "r") as difference:
                for line in difference.readlines():
                    if (result := re.search(pattern=PATTERN, string=line)):
                        yield (file.stem, next(iter(result.groups())))

    def differentiate(self):
        differences = collections.defaultdict(set)
        for operation, difference in self.generator():
            differences[operation].add(difference)
        differences = format(differences)

        Path(TEMPORARY).mkdir(exist_ok=True)
        with open(Path(TEMPORARY, f"{DIFFERENCES}.json"), "w") as file:
            file.write(to_json(differences))
        with open(Path(TEMPORARY, f"{DIFFERENCES}.markdown"), "w") as file:
            file.write(to_markdown(differences))
        
        return differences

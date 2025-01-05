import pathlib

from ..configuration import SOURCE, MATHEMATICS, COVER, DOCUMENT
from ..infrastructure.system import File
from .domain import Title



class Builder():
    def build(self):
        yield r"\documentclass{book}"
        for root, directories, files in pathlib.Path(SOURCE).walk():
            sources = (File(pathlib.Path.joinpath(root, file)) for file in files)
            sources = sorted(sources, key=lambda file: file.create_time)
            for source in sources:
                yield f"\\input{{{source}}}"
        yield f"\\input{{{DOCUMENT}/{COVER}}}"
        yield r"\begin{document}"
        yield r"\maketitle"
        yield r"\tableofcontents"
        for part in pathlib.Path(DOCUMENT).iterdir():
            for root, directories, files in part.walk():
                title = Title(root=root)
                yield f"{title.indent}\\{title.header}{{{title.description}}}"
                if files:
                    documents = (File(pathlib.Path.joinpath(root, file)) for file in files)
                    documents = sorted(documents, key=lambda file: file.create_time)
                    for document in documents:
                        yield f"{title.indent}\\include*{{{document}}}"
        yield r"\end{document}"

    def generate(self):
        with open(f"{MATHEMATICS}.tex", "w") as file:
            for line in self.build():
                file.write(f"{line}\n")

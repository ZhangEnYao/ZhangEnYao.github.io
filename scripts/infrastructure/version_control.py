import subprocess

from ..infrastructure.system import Path
from ..configuration import TEMPORARY, ADDITION, SUBTRACTION, DIFFERENCES



class VersionControl:
    @staticmethod
    def version_control():
        if not Path(".git").exists():
            subprocess.run("git init .", shell=True)
        subprocess.run("git add .", shell=True)
        subprocess.run('git commit --message="Work-In-Progress: work in progress"', shell=True)
    
    @staticmethod
    def differentiate():
        completed_process = subprocess.run("git rev-list HEAD --count", shell=True, capture_output=True)
        counts = int(completed_process.stdout)
        commit = "HEAD^" if counts > 1 else 'HEAD'
        Path(TEMPORARY).mkdir(exist_ok=True)
        subprocess.run(f''' git diff {commit} -- "document/*/*.tex" | grep '^+' > {TEMPORARY}/{ADDITION} ''', shell=True)
        subprocess.run(f''' git diff {commit} -- "document/*/*.tex" | grep '^-' > {TEMPORARY}/{SUBTRACTION} ''', shell=True)

build:
	python3 -B script.py --script="build"

clear:
	python3 -B script.py --script="clear"

ARGUMENTS = ""
query:
	python3 -B script.py --script="query" --arguments="$(ARGUMENTS)"

differentiate:
	python3 -B script.py --script="differentiate"

version_control: clear
	python3 -B script.py --script="version_control"

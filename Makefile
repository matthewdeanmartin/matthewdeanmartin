format:
	isort src
	black src
	mdformat src docs *.md

data:
	uv run gimc update-data

build:
	uv run gimc build

everything: data build format
	echo "everything"
	cp docs/md/README.en.md README.en.md

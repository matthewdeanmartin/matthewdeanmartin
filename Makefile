.PHONY: format
format:
	isort src
	black src
	mdformat src docs *.md

.PHONY: data
data:
	uv run gimc update-data

.PHONY: build
build:
	uv run gimc build

.PHONY: everything
everything: data build format
	echo "everything"
	cp docs/md/README.en.md README.en.md


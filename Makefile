format:
	isort src
	black src
	mdformat src docs *.md


data:
	uv run readme-make update-data

build:
	uv run readme-make build

everything: data build
	echo "everything"


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

.PHONY: run
run: everything
	python -m scripts.open_site

.PHONY: source
source:
	./scripts/make_source_data.sh
	./scripts/make_source_ui.sh
	./scripts/make_source.sh
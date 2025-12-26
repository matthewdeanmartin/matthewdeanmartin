.PHONY: test
test:
	uv run pytest src/tests

coverage:
	uv run pytest src/tests -vv -n 2 --cov=github_is_my_cms --cov-report=html --cov-fail-under 48 --cov-branch --cov-report=xml --junitxml=junit.xml -o junit_family=legacy --timeout=5 --session-timeout=600


.PHONY: format
format:
	uv run isort src
	uv run black src
	uv run mdformat src docs *.md

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
	uv run python -m scripts.open_site

.PHONY: source
source:
	./scripts/make_source_data.sh
	./scripts/make_source_ui.sh
	./scripts/make_source.sh

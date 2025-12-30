# Runnable tasks.

all: commands

## build: build HTML
build:
	@mccole build --src . --dst docs
	@touch docs/.nojekyll

## check: check project
check:
	@mccole check --src . --dst docs

## clean: clean up
clean:
	@find . -type f -name '*~' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r
	@find . -type d -name .pytest_cache | xargs rm -r
	@find . -type d -name .ruff_cache | xargs rm -r

## commands: show available commands (*)
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## format: format code
format:
	@ruff format .

## lint: check code
lint:
	@ruff check .

## serve: serve local website
serve:
	@python -m http.server --directory docs

[private]
default:
  @just --list

sync:
  uvx sync --group dev

# Run linter
lint *files:
  uvx ruff@latest check --output-format concise {{files}}

# Dry run formatter and output the diffs
fmt:
  uvx ruff@latest format --diff

# Run 'mypy' type-checker
mypy:
  uv run --group mypy -- mypy

# Run 'pyright' type-checker
pyright:
  uv run --group pyright -- pyright

build:
  uv build

image-name := "maya-stubs"

[private]
docker-build:
  docker build --platform linux/amd64 -t {{image-name}} .

# Run an interactive docker container
interactive: docker-build
  docker run -it --rm {{image-name}}

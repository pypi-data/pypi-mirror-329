# ethereal-py-sdk

**Welcome to ethereal-py-sdk!**

Python SDK for interacting with the Ethereal API.

## Getting started

Before you start, make sure you have installed [uv](https://docs.astral.sh/uv/getting-started/installation/):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then you can install the SDK and run the tests:

```bash
# Clone the project
git clone git@github.com:meridianxyz/ethereal-py-sdk.git

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run the linter
uv run ruff check --fix

# Run the example CLI
uv run python -i examples/cli.py
```

## Usage

Using the SDK using the REPL (example):

```python
import ethereal

rc = ethereal.RESTClient()
rc.list_products()
```

Or use the provided CLI:

```bash
cp .env.test .env

uv run python -i examples/cli.py

>>> rc.list_products()
```

## Generating Pydantic Type

Ethereal uses an OpenAPI spec to represent the API. You can generate Pydantic models from the OpenAPI spec using the `datamodel-codegen` tool:

```bash
# place a `spec.json` in the root of the project
uv run datamodel-codegen --input /path/to/api_spec.json \
  --output ethereal/models/generated.py \
  --input-file-type openapi \
  --openapi-scopes paths schemas parameters \
  --output-model-type pydantic_v2.BaseModel
```

## Documentation

Docs are created using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). To run the docs locally:

```bash
# serve
uv run mkdocs serve

# build
uv run mkdocs build
```

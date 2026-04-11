
<p align="center">
  <img src="assets/logo.png" alt="MoleQL logo" width="240" />
</p>


# MoleQL

> Expressive URL-query to MongoDB query conversion library.

[![CI](https://github.com/OneTesseractInMultiverse/moleql/actions/workflows/ci.yml/badge.svg)](https://github.com/OneTesseractInMultiverse/moleql/actions)
[![License](https://img.shields.io/github/license/OneTesseractInMultiverse/moleql.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/moleql.svg)](https://pypi.org/project/moleql)
[![Python Versions](https://img.shields.io/pypi/pyversions/moleql.svg)](https://pypi.org/project/moleql)

## Overview

MoleQL allows your REST APIs or data layers to accept
URL-style query strings (e.g. `?age>30&status=in(active,pending)`)
and converts them into MongoDB-compatible query dictionaries.
It supports filters, sorting, skip/limit, projection and text search.

Example:

```python
from moleql import parse

query = parse("age>30&country=US&name=/^John/i")
# yields:
# {
#   "filter": {"age": {"$gt": 30}, "country": "US", "name": {"$regex": "^John", "$options": "i"}},
#   "sort": None,
#   "skip": 0,
#   "limit": 0,
#   "projection": None
# }
```

## ✨ Features

- 🧠 Intuitive syntax: `=, !=, <, <=, >, >=`
- 📋 List operators: `in(...), ...`
- 🔍 Regex: `/pattern/flags → $regex + $options`
- 🧾 Pagination: `skip=10, limit=50`
- ⚙️ Sorting: `sort=-created_at,name`
- 🧩 Projection: `fields=name,email,age`
- 🔠 Text search: `text=free text here` or `$text=free text here`
- 🧱 Type casters: `custom value transformations`
- 🚫 Blacklist: skip parsing of restricted fields
- 🧪 Tested: full pytest coverage, Ruff linting

## 🧰 Installation

With uv (recommended):

```bash
uv add moleql
```

```bash
pip install moleql
```

## 🚀 Quick Start

```python
from moleql import parse

query = parse("age>30&country=US&name=/^John/i")
print(query)

# {
#   "filter": {
#       "age": {"$gt": 30},
#       "country": "US",
#       "name": {"$regex": "^John", "$options": "i"}
#   },
#   "sort": None,
#   "skip": 0,
#   "limit": 0,
#   "projection": None
# }
```

Extended example

```python
from moleql import parse

query = parse(
    "age>=18&status=in(active,pending)"
    "&sort=-created_at,name"
    "&skip=10&limit=20"
    "&fields=name,email,age"
)

```

Output:

```python
{
    "filter": {
        "age": {"$gte": 18},
        "status": {"$in": ["active", "pending"]}
    },
    "sort": [("created_at", -1), ("name", 1)],
    "skip": 10,
    "limit": 20,
    "projection": {"name": 1, "email": 1, "age": 1}
}

```

## 🔣 Supported Operators

|       Expression | Mongo Operator | Example                   |
|-----------------:|:---------------|:--------------------------|
|              `=` | direct match   | `age=20` → `{"age": 20}`  |
|             `!=` | `$ne`          | `status!=active`          |
|       `>` / `>=` | `$gt` / `$gte` | `score>=80`               |
|       `<` / `<=` | `$lt` / `$lte` | `price<10`                |
|        `in(...)` | `$in`          | `role=in(admin,user)`     |
|      `!=in(...)` | `$nin`         | `tier!=in(gold,platinum)` |
| `/pattern/flags` | `$regex`       | `name=/^Jo/i`             |
| `text=` or `$text=` | `$text`     | `text=free search text`   |
|        `fields=` | projection     | `fields=name,email`       |
|          `sort=` | sort directive | `sort=-created_at,name`   |

## 🧱 Quick API Reference

`parse(moleql_query: str, blacklist=None, casters=None) -> dict`

```python
from moleql import parse

parse("age>25&active=true")
```

Returns a dictionary with:
`filter`, `sort`, `skip`, `limit`, `projection`

`moleqularize(moleql_query: str, blacklist=None, casters=None) -> MoleQL`

Parse a MoleQL string and return the internal MoleQL object for
advanced inspection and debugging.

```python
from moleql import moleqularize

m = moleqularize("age>25")
print(m.mongo_query)

```

## 🧩 Custom Casters

You can define custom casters to control type conversions.

```python
from moleql import parse, get_casters


def to_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")


custom_casters = {"bool": to_bool}

q = parse("active=bool(true)&age>30", casters=custom_casters)

```

## 🧠 Design Philosophy

- Transparency — The query string is readable and reversible.
- Safety — No eval, injection-safe parsing.
- Extensibility — Easy to plug in custom handlers.
- Predictability — Every operator maps 1:1 to Mongo semantics.
- Minimal dependencies — Pure Python, no ODM required.

## ⚙️ Integration Examples

**FastAPI**

```python
from fastapi import FastAPI, Request
from moleql import parse
from pymongo import MongoClient

db = MongoClient()["app"]
app = FastAPI()


@app.get("/users")
def list_users(request: Request):
    q = parse(request.url.query.lstrip("?"))
    return list(db.users.find(q["filter"]))

```

**Flask**

```python
from flask import Flask, request, jsonify
from moleql import parse

app = Flask(__name__)


@app.get("/orders")
def orders():
    q = parse(request.query_string.decode())
    return jsonify(q)

```

## 🧪 Testing

Run the full suite using uv:

```bash
uv sync --all-extras --dev
uv run pytest -vv --cov=moleql --cov-report=term-missing --cov-fail-under=100

```

Generate coverage:

```bash
uv run pytest --cov=moleql --cov-report=term-missing --cov-fail-under=100

```

## 🧹 Code Quality

This repository uses:

 - Ruff — Linting + formatting (UP / pyupgrade rules)
 - pre-commit — automatic checks
 - pytest — testing
 - uv — environment & packaging

Set up hooks:
```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## 🧭 Roadmap

- [] Add exists(field) and between(a,b) operators
- [] Add optional CLI (moleql "age>20" --as-json)
- [] Extended docs and tutorials

🤝 Contributing

1. Fork this repository
2. Create your feature branch

    ```bash
    git checkout -b feat/awesome-change
    ```
3. Run formatting and tests

    ```bash
    uv run pre-commit run --all-files
    uv run pytest
    ```
4. Commit and push your changes
5. Open a Pull Request 🚀

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.


## 🌟 Acknowledgments

Built and maintained by [@OneTesseractInMultiverse](https://github.com/OneTesseractInMultiverse)
Inspired by the need for readable, typed, and safe Mongo queries in API
environments.

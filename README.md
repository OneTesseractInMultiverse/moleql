# MoleQL

> Convert URL query strings into safe, composable **MongoDB** queries.

[![CI](https://github.com/OneTesseractInMultiverse/moleql/actions/workflows/ci.yml/badge.svg)](https://github.com/OneTesseractInMultiverse/moleql/actions)
[![License](https://img.shields.io/github/license/OneTesseractInMultiverse/moleql.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](#)
[![uv](https://img.shields.io/badge/uv-managed-brightgreen.svg)](#)

MoleQL lets your REST endpoints accept expressive filters like:

```bash
?age>30&country=US&name=/^John/i&status=in(active,pending)
```

...and converts them into a MongoDB query document:

```python
{
    "age": {"$gt": 30},
    "country": "US",
    "name": {"$regex": "^John", "$options": "i"},
    "status": {"$in": ["active", "pending"]}
}
```
## ✨ Features

 - Operators: =, !=, <, <=, >, >=, in(...), nin(...), /regex/flags
 - Nested fields: dotted notation (user.age>=21)
 - Safe by default: no eval, controlled regex flags
 - Extensible: register custom operators
 - Framework-friendly: tiny API, easy to embed in FastAPI/Flask
 - uv-first: lockfile + fast local/CI installs

> Related art / terminology: MongoDB’s Atlas queryString operator (search layer) differs from MoleQL’s request-filter parsing; MoleQL targets classic MQL filters. See Atlas docs for the search operator if you need full-text search semantics.
MongoDB

## 📦 Install

With uv (recommended):

```bash
 uv add moleql
```
Or with pip:

```bash
 pip install moleql
```

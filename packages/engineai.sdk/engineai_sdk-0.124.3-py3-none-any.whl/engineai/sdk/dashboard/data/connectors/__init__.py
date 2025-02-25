"""Connectors for fetching data from various sources."""

from .duck_db.duck_db import DuckDB
from .http.http_get import HttpGet

__all__ = ["HttpGet", "DuckDB"]

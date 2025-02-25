"""Connectors dependencies for the dashboard."""

from .duck_db import DuckDBConnectorDependency
from .http import HttpConnectorDependency

__all__ = ["HttpConnectorDependency", "DuckDBConnectorDependency"]

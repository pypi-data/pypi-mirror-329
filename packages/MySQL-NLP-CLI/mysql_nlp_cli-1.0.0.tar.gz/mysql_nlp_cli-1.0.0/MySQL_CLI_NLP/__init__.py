"""
MySQL_CLI_NLP

A Python package that converts natural language commands into MySQL database schemas
through both CLI and interactive modes.
"""

__version__ = "1.0.0"
__all__ = [
    'DatabaseManager',
    'NLPProcessor',
    'DatabaseError',
    'DatabaseCreationError',
    'NLPParseError',
    'SchemaValidationError',
    'DatabaseDefinition',
    'TableDefinition',
    'ColumnDefinition'
]

from .cli import main
from .database import DatabaseManager
from .nlp_processor import NLPProcessor
from .exceptions import (
    DatabaseError,
    DatabaseCreationError,
    NLPParseError,
    SchemaValidationError
)
from .schema import DatabaseDefinition, TableDefinition, ColumnDefinition
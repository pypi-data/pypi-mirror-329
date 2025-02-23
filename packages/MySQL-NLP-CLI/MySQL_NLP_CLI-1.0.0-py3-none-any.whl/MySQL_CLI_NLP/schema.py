# -------------------- schema.py --------------------
from dataclasses import dataclass
from typing import List, Optional
import re

from MySQL_CLI.MySQL_CLI_NLP.exceptions import SchemaValidationError


@dataclass
class ColumnDefinition:
    name: str
    data_type: str
    length: Optional[int] = None
    is_primary: bool = False
    is_nullable: bool = True
    default: Optional[str] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not re.match(r'^[\w]+$', self.name):
            raise SchemaValidationError(f"Invalid column name: {self.name}")
        if self.data_type.upper() not in SUPPORTED_TYPES:
            raise SchemaValidationError(f"Unsupported data type: {self.data_type}")

SUPPORTED_TYPES = {
    'VARCHAR', 'INT', 'FLOAT', 'DOUBLE', 'DATE',
    'DATETIME', 'BOOLEAN', 'TEXT', 'BLOB'
}

@dataclass
class TableDefinition:
    name: str
    columns: List[ColumnDefinition]
    engine: str = 'InnoDB'
    charset: str = 'utf8mb4'
    collate: str = 'utf8mb4_0900_ai_ci'

    def __post_init__(self):
        if not re.match(r'^[\w]+$', self.name):
            raise SchemaValidationError(f"Invalid table name: {self.name}")
        primary_columns = [c for c in self.columns if c.is_primary]
        if len(primary_columns) > 1:
            raise SchemaValidationError("Multiple primary keys defined")

@dataclass
class DatabaseDefinition:
    name: str
    tables: List[TableDefinition]
    charset: str = 'utf8mb4'
    collation: str = 'utf8mb4_0900_ai_ci'

    def __post_init__(self):
        if not re.match(r'^[\w]+$', self.name):
            raise SchemaValidationError(f"Invalid database name: {self.name}")


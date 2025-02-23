# -------------------- nlp_processor.py --------------------
import re
from MySQL_CLI.MySQL_CLI_NLP.exceptions import NLPParseError
from MySQL_CLI.MySQL_CLI_NLP.schema import ColumnDefinition, DatabaseDefinition, TableDefinition
import spacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Span
from typing import List


class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self._initialize_patterns()
        self.type_mapping = {
            'str': 'VARCHAR', 'string': 'VARCHAR',
            'int': 'INT', 'integer': 'INT', 'number': 'INT',
            'float': 'FLOAT', 'double': 'DOUBLE',
            'date': 'DATE', 'datetime': 'DATETIME',
            'bool': 'BOOLEAN', 'text': 'TEXT'
        }

    def _initialize_patterns(self):
        self.matcher = Matcher(self.nlp.vocab)
        patterns = {
            'CREATE_DATABASE': [
                [{"LOWER": {"IN": ["create", "make"]}}, 
                 {"LOWER": "database"}, 
                 {"LOWER": "named"}, 
                 {"ENT_TYPE": "DATABASE_NAME"}]
            ],
            'ADD_TABLE': [
                [{"LOWER": "add"}, {"LOWER": "table"}, 
                 {"ENT_TYPE": "TABLE_NAME"}, {"LOWER": "with"}, 
                 {"LOWER": "columns"}, {"ENT_TYPE": "COLUMNS"}]
            ]
        }
        for key, pattern in patterns.items():
            self.matcher.add(key, pattern)

        # Add custom entity recognizer
        ruler = self.nlp.add_pipe("entity_ruler")
        patterns = [
            {"label": "DATABASE_NAME", "pattern": [{"TEXT": {"REGEX": "^[\w]+$"}}]},
            {"label": "TABLE_NAME", "pattern": [{"TEXT": {"REGEX": "^[\w]+$"}}]},
            {"label": "COLUMNS", "pattern": [{"TEXT": {"REGEX": "\(.*\)"}}]}
        ]
        ruler.add_patterns(patterns)

    def _parse_column(self, col_text: str) -> ColumnDefinition:
        # Enhanced parsing with regex
        col_regex = re.compile(
            r"(\w+)\s+"                   # Column name
            r"(\w+)(?:\((\d+)\))?"        # Data type and length
            r"(?:\s+(PRIMARY\s+KEY))?"    # Primary key
            r"(?:\s+(NOT\s+NULL))?"       # Nullability
            r"(?:\s+DEFAULT\s+([\w']+))?" # Default value
        )
        match = col_regex.match(col_text.strip())
        if not match:
            raise NLPParseError(f"Invalid column syntax: {col_text}")

        name, dtype, length, pk, null, default = match.groups()
        return ColumnDefinition(
            name=name,
            data_type=self.type_mapping.get(dtype.lower(), 'VARCHAR'),
            length=int(length) if length else None,
            is_primary=bool(pk),
            is_nullable=not bool(null),
            default=default.strip("'") if default else None
        )

    def parse_command(self, text: str) -> DatabaseDefinition:
        doc = self.nlp(text)
        db_name = None
        tables = []

        # Extract database name
        for ent in doc.ents:
            if ent.label_ == "DATABASE_NAME":
                db_name = ent.text
                break

        # Extract tables and columns
        for match_id, start, end in self.matcher(doc):
            if self.nlp.vocab.strings[match_id] == "ADD_TABLE":
                table_ent = next(e for e in doc.ents if e.label_ == "TABLE_NAME")
                columns_ent = next(e for e in doc.ents if e.label_ == "COLUMNS")
                
                columns = [
                    self._parse_column(col.strip()) 
                    for col in columns_ent.text.strip("()").split(",")
                ]
                tables.append(TableDefinition(name=table_ent.text, columns=columns))

        if not db_name or not tables:
            raise NLPParseError("Incomplete schema definition")

        return DatabaseDefinition(name=db_name, tables=tables)

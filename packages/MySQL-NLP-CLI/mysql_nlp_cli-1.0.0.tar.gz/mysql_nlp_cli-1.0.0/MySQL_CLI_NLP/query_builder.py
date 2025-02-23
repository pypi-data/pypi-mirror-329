# -------------------- query_builder.py --------------------
from MySQL_CLI.MySQL_CLI_NLP.schema import DatabaseDefinition, TableDefinition
from mysql.connector import escape_string

class SQLQueryBuilder:
    @staticmethod
    def create_database(db_def: DatabaseDefinition) -> str:
        return (
            f"CREATE DATABASE IF NOT EXISTS `{escape_string(db_def.name)}` "
            f"CHARACTER SET {db_def.charset} COLLATE {db_def.collation}"
        )

    @staticmethod
    def create_table(table: TableDefinition) -> str:
        columns = []
        for col in table.columns:
            col_def = [
                f"`{escape_string(col.name)}`",
                f"{col.data_type}"
            ]
            if col.length:
                col_def[1] += f"({col.length})"
            if col.is_primary:
                col_def.append("PRIMARY KEY")
            if not col.is_nullable:
                col_def.append("NOT NULL")
            if col.default:
                col_def.append(f"DEFAULT {escape_string(col.default)}")
                
            columns.append(" ".join(col_def))
        
        return (
            f"CREATE TABLE IF NOT EXISTS `{escape_string(table.name)}` (\n"
            f"{',\n'.join(columns)}\n) "
            f"ENGINE={table.engine} "
            f"DEFAULT CHARSET={table.charset}"
        )


# -------------------- database.py --------------------#
import mysql.connector 
from mysql.connector import errorcode, pooling
import logging
from contextlib import contextmanager
from typing import List
from .query_builder import SQLQueryBuilder
from .schema import DatabaseDefinition
from .exceptions import DatabaseCreationError

class DatabaseManager:
    def __init__(self, user: str, password: str, 
                 host: str = 'localhost', port: int = 3306,
                 pool_size: int = 5):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="schema_pool",
            pool_size=pool_size,
            host=host,
            port=port,
            user=user,
            password=password,
            autocommit=False
        )
        self.logger = logging.getLogger(__name__)
        self.query_builder = SQLQueryBuilder()

    @contextmanager
    def _get_connection(self):
        conn = self.pool.get_connection()
        try:
            yield conn
        finally:
            conn.close()

    def create_database(self, definition: DatabaseDefinition, dry_run: bool = False):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Create database
                db_query = self.query_builder.create_database(definition)
                self._execute(cursor, db_query, dry_run)
                
                # Switch database
                use_query = f"USE `{definition.name}`"
                self._execute(cursor, use_query, dry_run)

                # Create tables
                for table in definition.tables:
                    table_query = self.query_builder.create_table(table)
                    self._execute(cursor, table_query, dry_run)

                if not dry_run:
                    conn.commit()

        except mysql.connector.Error as err:
            conn.rollback()
            self.logger.error(f"Database operation failed: {err}")
            raise DatabaseCreationError(f"MySQL Error: {err}", original_error=err)
        except Exception as err:
            self.logger.critical(f"Unexpected error: {err}")
            raise

    def _execute(self, cursor, query: str, dry_run: bool):
        self.logger.debug(f"Executing query: {query}")
        if dry_run:
            print(f"[DRY RUN] {query}")
            return
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                self.logger.warning(f"Table already exists: {err}")
            else:
                raise

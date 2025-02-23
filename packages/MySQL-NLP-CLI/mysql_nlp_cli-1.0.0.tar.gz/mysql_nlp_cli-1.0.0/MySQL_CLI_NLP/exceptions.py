# -------------------- exceptions.py --------------------
class DatabaseError(Exception):
    """Base exception for database-related errors"""
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error

class DatabaseCreationError(DatabaseError):
    """Errors during database creation"""

class DatabaseConnectionError(DatabaseError):
    """Connection-related errors"""

class NLPParseError(Exception):
    """Natural language parsing failures"""

class SchemaValidationError(Exception):
    """Invalid schema configuration"""

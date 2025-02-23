# -------------------- cli.py --------------------
import argparse
from typing import List, Optional
import getpass
import logging
from pathlib import Path
import re
from .nlp_processor import NLPProcessor
from .database import DatabaseManager
from .schema import SUPPORTED_TYPES, DatabaseDefinition, TableDefinition, ColumnDefinition
from .exceptions import SchemaValidationError, NLPParseError, DatabaseError

def configure_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("schema_creator.log")]
    )

class InteractiveCLI:
    @staticmethod
    def prompt_with_validation(prompt_text: str, validator: callable, error_msg: str):
        while True:
            try:
                value = input(prompt_text).strip()
                validator(value)
                return value
            except ValueError as e:
                print(f"Error: {e}. Please try again.")

    @staticmethod
    def collect_database_info() -> DatabaseDefinition:
        print("\n=== MySQL Schema Creator - Interactive Mode ===")
        
        # Database name
        db_name = InteractiveCLI.prompt_with_validation(
            "\nEnter database name: ",
            lambda n: re.match(r'^[\w]+$', n) or ValueError("Invalid database name"),
            "Invalid database name"
        )

        tables: List[TableDefinition] = []
        while True:
            tables.append(InteractiveCLI.collect_table_info())
            if not input("\nAdd another table? (y/N): ").lower().startswith('y'):
                break

        return DatabaseDefinition(name=db_name, tables=tables)

    @staticmethod
    def collect_table_info() -> TableDefinition:
        table_name = InteractiveCLI.prompt_with_validation(
            "\nEnter table name: ",
            lambda n: re.match(r'^[\w]+$', n) or ValueError("Invalid table name"),
            "Invalid table name"
        )

        columns: List[ColumnDefinition] = []
        while True:
            columns.append(InteractiveCLI.collect_column_info())
            if not input("\nAdd another column? (Y/n): ").lower().startswith('n'):
                break

        return TableDefinition(name=table_name, columns=columns)

    @staticmethod
    def collect_column_info() -> ColumnDefinition:
        print("\nNew column details:")
        name = InteractiveCLI.prompt_with_validation(
            "  Column name: ",
            lambda n: re.match(r'^[\w]+$', n) or ValueError("Invalid column name"),
            "Invalid column name"
        )

        data_type = InteractiveCLI.prompt_with_validation(
            "  Data type (VARCHAR, INT, DATE, etc.): ",
            lambda t: t.upper() in SUPPORTED_TYPES or ValueError("Unsupported type"),
            "Unsupported data type"
        ).upper()

        length: Optional[int] = None
        if data_type in ['VARCHAR', 'CHAR', 'DECIMAL']:
            length_str = input("  Length/precision (optional): ").strip()
            if length_str:
                length = int(length_str)

        is_primary = input("  Is primary key? [y/N]: ").lower().startswith('y')
        is_nullable = input("  Nullable? [Y/n]: ").lower() not in ['n', 'no']
        default = input("  Default value (optional): ").strip() or None

        try:
            return ColumnDefinition(
                name=name,
                data_type=data_type,
                length=length,
                is_primary=is_primary,
                is_nullable=is_nullable,
                default=default
            )
        except SchemaValidationError as e:
            print(f"Validation error: {e}")
            return InteractiveCLI.collect_column_info()

def main():
    parser = argparse.ArgumentParser(
        description="Natural Language MySQL Schema Creator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Input parameters
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-t", "--text", help="Natural language command")
    input_group.add_argument("-f", "--file", type=Path, help="Input file with commands")
    input_group.add_argument("-i", "--interactive", action="store_true", 
                           help="Start interactive mode")

    # Connection parameters
    parser.add_argument("-u", "--user", required=True, help="MySQL username")
    parser.add_argument("-H", "--host", default="localhost", help="MySQL host")
    parser.add_argument("-P", "--port", type=int, default=3306, help="MySQL port")
    parser.add_argument("--pool-size", type=int, default=5, 
                       help="Connection pool size")

    # Options
    parser.add_argument("--dry-run", action="store_true", 
                       help="Generate SQL without execution")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Enable verbose logging")

    args = parser.parse_args()
    configure_logging(args.verbose)

    try:
        
        if args.interactive:
            db_def = InteractiveCLI.collect_database_info()
        else:
        # Read input
            text = args.file.read_text() if args.file else args.text

        # Process NLP
            processor = NLPProcessor()
            db_def = processor.parse_command(text)

        # Get password securely
            password = getpass.getpass(prompt="MySQL password: ")

        # Create database
            db_manager = DatabaseManager(
                user=args.user,
                password=password,
                host=args.host,
                port=args.port,
                pool_size=args.pool_size
            )
            db_manager.create_database(db_def, args.dry_run)

            logging.info("Schema creation completed successfully!")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    except SchemaValidationError as e:
            logging.error(f"Schema validation failed: {e}")
    except NLPParseError as e:
            logging.error(f"Input parsing error: {e}")
    except DatabaseError as e:
            logging.error(f"Database error: {e}\nOriginal error: {e.original_error}")
    except Exception as e:
            logging.critical(f"Unexpected error: {e}")

# -------------------- cli.py --------------------

if __name__ == "__main__":
    main()  # Run the main function

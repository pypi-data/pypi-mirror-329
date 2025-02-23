*README.md*

# Natural Language MySQL Schema Creator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package that converts natural language commands into MySQL database schemas through both CLI and interactive modes.

## Features

- 🗣️ Natural language processing for schema creation
- 🔒 Secure database connections with parameterized queries
- 💻 Interactive CLI mode with guided prompts
- 📝 Support for both text input and file input
- 🛠️ Schema validation and error recovery
- 🔄 Connection pooling for better performance
- 🧪 Dry-run mode for SQL preview

## Installation

bash
pip install MySQL_NLP_CLI
python -m spacy download en_core_web_sm


## Usage

### Command Line Interface

bash
# Natural language input
mysql_nlp_cli -t "Create database 'ecommerce' with table users (id int primary key)" -u root

# File input
mysql_nlp_cli -f schema.txt -u root --dry-run

# Interactive mode
mysql_nlp_cli -i -u root


### Natural Language Examples

Input:
text
Create database 'inventory' with tables:
- products (id int primary key, name varchar(255) not null, price decimal(10,2))
- orders (order_id int auto_increment, product_id int, quantity int)


Generated SQL:
sql
CREATE DATABASE inventory CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE inventory;

CREATE TABLE products (
  id INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE orders (
  order_id INT AUTO_INCREMENT,
  product_id INT,
  quantity INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


### Interactive Mode Demo

text
$  mysql_nlp_cli -i -u root

=== MySQL Schema Creator ===

Database name: my_shop

Add table? [Y/n]: y

Table name: customers

Column name: id
Data type: INT
Primary key? [y/N]: y
Nullable? [Y/n]: n

Add another column? [Y/n]: y

Column name: email
Data type: VARCHAR
Length: 255
Nullable? [Y/n]: n
Unique constraint? [y/N]: y

[1] Continue to database creation
[2] Preview SQL
[3] Cancel

Choice: 2

Generated SQL:
...


## Configuration

Environment variables (optional):
env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root


## Features

- **Natural Language Processing**
  - Automatic type conversion
  - Constraint detection (primary key, nullability)
  - Multi-table support
  - Complex column definitions

- **Security**
  - Password masking
  - SQL injection prevention
  - Connection encryption
  - Schema validation

- **Interactive Mode**
  - Step-by-step guidance
  - Real-time validation
  - Error recovery
  - SQL preview

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -am 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

**Q: Getting "Language model not found" error**
bash
python -m spacy download en_core_web_sm


**Q: MySQL connection issues**
- Verify MySQL server is running
- Check firewall settings
- Validate user permissions

**Q: Schema validation errors**
- Ensure names follow [a-zA-Z0-9_] pattern
- Check for duplicate primary keys
- Verify supported data types


This documentation provides users with comprehensive information about the package while maintaining professional formatting and clear organization. The README includes:

1. Badges for quick info
2. Feature highlights
3. Installation instructions
4. Usage examples
5. Configuration guidance
6. Development guidelines
7. Troubleshooting common issues
8. License information

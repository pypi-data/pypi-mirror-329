"""
Havinosh Data Loader
--------------------
A Python package for dynamically loading CSV files into PostgreSQL tables.

Modules:
- config: Database configuration settings.
- db_utils: Functions for database connection, table creation, and data insertion.
- process_csv: Functions for processing CSV files.
"""

from .config import DB_CONFIG
from .db_utils import create_table, insert_data, get_db_connection
from .process_csv import process_csv

__all__ = ["DB_CONFIG", "create_table", "insert_data", "get_db_connection", "process_csv"]

__version__ = "0.0.1"
__author__ = "Vishal Singh Sangral"
__email__ = "support@havinosh.com"
__license__ = "MIT"

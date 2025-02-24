import psycopg2
import pandas as pd
from havinosh_data_loader.config import DB_CONFIG
from havinosh_data_loader.logger import logger
from havinosh_data_loader.exception import LoaderException
import sys

def get_db_connection():
    """Establish PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("Connected to PostgreSQL database")
        return conn
    except Exception as e:
        raise LoaderException(e, sys)

def create_table(table_name, df):
    """Dynamically create a table based on CSV structure"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
        query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Table '{table_name}' created successfully!")
    except Exception as e:
        raise LoaderException(e, sys)

def insert_data(table_name, df):
    """Insert data into the PostgreSQL table"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            values = tuple(row.astype(str))  # Convert all values to string to avoid type errors
            query = f'INSERT INTO "{table_name}" VALUES {values};'
            cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Data inserted into '{table_name}' successfully!")
    except Exception as e:
        raise LoaderException(e, sys)

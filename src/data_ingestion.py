# ------------------------------------------
# Main entry point for running the workflow
# ------------------------------------------
import logging
from typing import Optional, Tuple
import time
from paths import CSV_FILES
# from logging_manager import Loggers
import psycopg2
from config import DB_connection, features_types
from psycopg2 import OperationalError
from psycopg2 import sql
import re
import pandas as pd

class Ingestor:
    def __init__(self, logger):
        self.logger = logger
        self.schema = "bronze"
        

    def read_csv_file(self, csv_path):
        """
        Loads CSV into a pandas DataFrame.
        Handles file encoding issues and reports number of rows/columns read.
        """
        self.logger.info("Reading CSV from %s ...", csv_path)
        try:
            df = pd.read_csv(str(csv_path), encoding='utf-8')
            self.logger.info("CSV loaded: %d rows x %d columns.", getattr(df, "shape", (0, 0))[0], getattr(df, "shape", (0, 0))[1])
            return df
        except Exception as e:
            self.logger.error("Unexpected error reading CSV file: %s", csv_path)
            raise
    
    def get_dtypes_of_columns(self, df,  table_name):
        # self.ingestion_logger.info("Extracting datatypes")
        columns_sql = []
        table_overrides = features_types.SCHEMA_OVERRIDES.get(table_name, {})
        for col_name, dtype in df.dtypes.items():
            if col_name in table_overrides:
                pg_type = table_overrides[col_name]
            else:
                pg_type = features_types.TYPE_MAPPING.get(str(dtype), "TEXT")  # Default to TEXT if unknown type
            columns_sql.append(f"{col_name} {pg_type}")

        # Join all column definitions into the CREATE TABLE statement
        columns_sql_str = ",\n    ".join(columns_sql)
        return columns_sql_str

    def execute_create_table_sql_query(self, cur, create_table_sql):
        self.logger.info("Constructing table")
        try:
            cur.execute(create_table_sql)
            self.logger.info("Table constructed.")
        except Exception as e:
            self.logger.exception("Failed to create table: %s", e)
            raise

    def generate_create_table_sql(self, df, cur, table_name):
        """
        Generates a SQL CREATE TABLE statement based on the DataFrame's columns and types.

        Args:
            df: pandas DataFrame containing the CSV data
            schema: schema name in PostgreSQL
            table_name: name of the table to create

        Returns:
            A string containing the SQL CREATE TABLE statement
        """
        self.logger.info("Generating CREATE TABLE statement for %s.%s ...", self.schema, table_name)

        try:
            columns_sql_str = self.get_dtypes_of_columns(df,  table_name)

            create_table_sql = f"""
            DROP TABLE IF EXISTS {self.schema}.{table_name} CASCADE;
            CREATE TABLE {self.schema}.{table_name} (
                {columns_sql_str}
            );
            """
            self.logger.info("CREATE TABLE SQL generated successfully for table '%s.%s'", self.schema, table_name)
            return create_table_sql.strip()
        
        except Exception as e:
            self.logger.exception("Failed to generate CREATE TABLE SQL: %s", e)
            raise
    
    def load_csv_data_into_table(self, cur, csv_path, table_name):
        """
        Loads data from a CSV file into a PostgreSQL table using COPY.

        Args:
            self: Class instance containing ingestion_logger
            cur: psycopg2 cursor object
            csv_path: Path to the CSV file
            schema: Target schema in PostgreSQL
            table_name: Target table in PostgreSQL

        Raises:
            Exception if the COPY command fails
        """
        self.logger.info("Loading CSV data into %s.%s ...", self.schema, table_name)

        try:

            with open(str(csv_path), "r", encoding="utf-8") as f:
                cur.copy_expert(
                    sql.SQL(
                        "COPY {}.{} FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')"
                    ).format(
                        sql.Identifier(self.schema),
                        sql.Identifier(table_name)
                    ),
                    f
                )

            self.logger.info("Data loaded successfully into %s.%s", self.schema, table_name)

        except Exception as e:
            self.logger.exception(
                "Failed to load CSV into %s.%s: %s", self.schema, table_name, e
            )
            raise
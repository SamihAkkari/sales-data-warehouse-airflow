import logging
import os

class LoggingConfig:
    STAGES = ["ingestion", "bronze", "silver", "gold"]
    LEVEL = logging.INFO
    FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    HANDLERS = {
        "rotating_file": {
            "max_bytes": 5_000_000, "backup_count": 3
            },
        }
    PROPAGATE_STATUS = False

class DB_connection:
    user_name = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    database_name = os.environ.get("POSTGRES_DB")
    host = os.environ.get("POSTGRES_HOST")
    port = os.environ.get("POSTGRES_PORT")

class features_types:
    TYPE_MAPPING = {
        "int64": "BIGINT",
        "int32": "INTEGER",
        "float64": "DOUBLE PRECISION",
        "float32": "REAL",
        "object": "TEXT",
        "bool": "BOOLEAN",
        "datetime64[ns]": "Date"
    }
    SCHEMA_OVERRIDES = {
        "customers": {
            "cst_id": "BIGINT",
            "cst_key": "TEXT",
            "cst_firstname": "TEXT",
            "cst_lastname": "TEXT",
            "cst_material_status": "TEXT",
            "cst_gndr": "TEXT",
            "created_at": "TEXT"
        },
        "products": {
            "prd_id": "BIGINT",
            "prd_key": "TEXT",
            "prd_key": "TEXT",
            "prd_cost": "BIGINT",
            "prd_line": "TEXT",
            "prd_start_dt": "TEXT",
            "prd_end_dt": "TEXT"

        },
        "sales": {
            "sls_ord_num": "TEXT",
            "sls_prd_key": "TEXT",
            "sls_cust_id": "BIGINT",
            "sls_order_dt": "BIGINT",
            "sls_ship_dt": "BIGINT",
            "sls_due_dt": "BIGINT",
            "sls_sales": "BIGINT",
            "sls_quantity": "BIGINT",
            "sls_price": "BIGINT"
        },

        "cust" : {
            "cid" : "TEXT",
            "bdate": "TEXT",
            "gen": "TEXT"
        },

        "loc": {
            "cid": "TEXT",
            "centry": "TEXT",
        },

        "px": {
            "id": "TEXT",
            "cat": "TEXT",
            "subcat": "TEXT",
            "maintenance": "TEXT"
        }
    }


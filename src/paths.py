import os
from pathlib import Path

# -----------------------------
# 1) Workspace root
# -----------------------------
WORKSPACE_ROOT = Path(os.environ.get("WORKSPACE_ROOT", "/opt/airflow"))

# -----------------------------
# 2) Dataset directory
# -----------------------------
DATASET_DIR = WORKSPACE_ROOT / "Dataset"
CSV_FILES = {
    "customers": DATASET_DIR / "customers_dataset.csv",
    "products": DATASET_DIR / "products_dataset.csv",
    "sales": DATASET_DIR / "sales_dataset.csv", 
    "cust": DATASET_DIR / "CUST_AZ12.csv",
    "loc": DATASET_DIR / "LOC_A101.csv",
    "px": DATASET_DIR / "PX_CAT_G1V2.csv"
    }

# -----------------------------
# 3) Log directory
# -----------------------------
# LOG_DIR = WORKSPACE_ROOT / "logs"
# LOG_FILES = {
#     "app": LOG_DIR / "app.log",
# }
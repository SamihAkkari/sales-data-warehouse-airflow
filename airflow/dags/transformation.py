from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


DBT_PROFILES_project_DIR = "/opt/airflow/dbt_project"


default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 8, 25),
    "depends_on_past": False
}

# Define your models
silver_models = ["customers", "products", "sales", "cust", "px", "loc"]
gold_models_dependant_on_silver = ["dim_customers", "dim_products", "fact_sales"]


transformation_dag = DAG(
    dag_id="Medallion_data_transformation",
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

# Dynamically create one task per silver model
silver_tasks = {}
for model in silver_models:
    task = BashOperator(
        task_id=f"dbt_silver_{model}",
        bash_command=f"""
        echo "Starting dbt run for model: {model}"
        dbt run --profiles-dir {DBT_PROFILES_project_DIR} --project-dir {DBT_PROFILES_project_DIR} --select {model}
        echo "Completed dbt run for model: {model}"
        """,
        dag = transformation_dag
    )
    silver_tasks[model] = task

# Dynamically create one task per gold model
gold_tasks = {}
for model in gold_models_dependant_on_silver:
    task = BashOperator(
        task_id=f"dbt_gold_{model}",
        bash_command=f"""
        echo "Starting dbt run for model: {model}"
        dbt run --profiles-dir {DBT_PROFILES_project_DIR} --project-dir {DBT_PROFILES_project_DIR} --select {model}
        echo "Completed dbt run for model: {model}"
        """,
        dag = transformation_dag
    )
    gold_tasks[model] = task

[silver_tasks["customers"], silver_tasks["cust"], silver_tasks["loc"]] >> gold_tasks["dim_customers"]
[silver_tasks["products"], silver_tasks["px"]] >> gold_tasks["dim_products"]
[gold_tasks["dim_customers"], gold_tasks["dim_products"]] >> gold_tasks["fact_sales"]
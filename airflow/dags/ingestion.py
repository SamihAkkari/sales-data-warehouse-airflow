from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from data_ingestion import Ingestor
from paths import CSV_FILES
import logging


def ingest_table(table_name, csv_path):
    logger = logging.getLogger("data_ingestion.task")
    
    logger.info ("Connecting to the database")
    hook = PostgresHook(postgres_conn_id="postgres_conn_id")
    conn = hook.get_conn()
    cur = conn.cursor()
    logger.info ("Connection to the database succeeded")

    ingestor = Ingestor(logger)
    df = ingestor.read_csv_file(csv_path)
    create_table_query = ingestor.generate_create_table_sql(df, cur, table_name)
    ingestor.execute_create_table_sql_query(cur, create_table_query)
    ingestor.load_csv_data_into_table(cur, csv_path, table_name)
    conn.commit()
    cur.close()
    conn.close()


data_ingestion_dag = DAG(
    dag_id = "Data_ingestion",
    description = "etc."
)


create_schema = PostgresOperator (
        task_id = "create_schema",
        postgres_conn_id="postgres_conn_id",
        sql = """
        CREATE SCHEMA IF NOT EXISTS bronze;
        """,
        dag = data_ingestion_dag
    )

# dynamically create one task per table
ingestion_tasks = []
for table_name, csv_path in CSV_FILES.items():
    task = PythonOperator(
        task_id=f'ingest_{table_name}',
        python_callable=ingest_table,
        op_args=[table_name, csv_path],
        dag=data_ingestion_dag,
    )
    ingestion_tasks.append(task)

create_schema >> ingestion_tasks
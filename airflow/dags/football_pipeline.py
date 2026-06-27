from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.insert(0, '/opt/airflow')
from ingestion.load_statsbomb import main

with DAG(
    dag_id='football_pipeline',
    schedule='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    ingesta = PythonOperator(
        task_id='load_statsbomb',
        python_callable=main,
    )

    dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='cd /opt/airflow/football_dw && dbt run --profiles-dir /opt/airflow/football_dw',
)

    dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='cd /opt/airflow/football_dw && dbt test --profiles-dir /opt/airflow/football_dw',
)
    ingesta >> dbt_run >> dbt_test
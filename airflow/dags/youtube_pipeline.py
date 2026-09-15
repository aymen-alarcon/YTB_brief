from airflow import DAG
from datetime import datetime
from airflow.providers.standard.operators.python import PythonOperator

with DAG(dag_id="youtube_pipeline", start_date=datetime(2026, 9, 16), schedule_interval="@daily", catchup=False) as dag:

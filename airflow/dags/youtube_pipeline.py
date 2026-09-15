from airflow import DAG
from datetime import datetime
from airflow.operators import annotations

with DAG(dag_id="youtube_pipeline", start_date=datetime(2026, 9, 16), schedule_interval="@daily", catchup=False) as dag:

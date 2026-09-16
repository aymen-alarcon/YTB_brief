import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow")

from include.extract import youtube_extract as extract_videos
from include.load import youtube_load as load_videos
from include.transform import youtube_transform as transform_videos

with DAG(
    dag_id="youtube_pipeline",
    start_date=datetime(2026, 9, 16),
    schedule="@hourly",
    catchup=False
) as dag:

    create_table = PythonOperator(
        task_id="create",
        python_callable=load_videos.create_table,
    )

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract_videos.extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_videos.transform,
    )

    create_table >> extract_task >> transform_task 

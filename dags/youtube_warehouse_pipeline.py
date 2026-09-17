import os
import sys
import json
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append("/opt/airflow")

from include.load import youtube_load as load_videos
from include.transform import youtube_transform as transform_videos

def read_json_file():
    file_path = "/opt/airflow/data/data.json"
    with open(file_path, "r") as f:
        return json.load(f)

with DAG(
    dag_id="youtube_warehouse_pipeline",
    start_date=datetime(2026, 9, 16),
    schedule=None,
    catchup=False
) as dag:

    read_json_task = PythonOperator(
        task_id="read_json",
        python_callable=read_json_file
    )

    create_staging_area = PythonOperator(
        task_id="create_staging",
        python_callable=load_videos.create_staging_table
    )

    load_staging_area = PythonOperator(
        task_id="load_staging",
        python_callable=load_videos.load_staging_table,
        op_args=[read_json_task.output]
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_videos.transform,
        op_args=[load_staging_area.output]
    )

    create_core_area = PythonOperator(
        task_id="create_core",
        python_callable=load_videos.create_core_table
    )

    load_core_area = PythonOperator(
        task_id="load_core",
        python_callable=load_videos.load_core_table,
        op_args=[read_json_task.output]
    )

    read_json_task >> create_staging_area >> load_staging_area >> transform_task >> create_core_area >> load_core_area

import os
import sys
import json
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.append("/opt/airflow")

from include.extract import youtube_extract as extract_videos

def generate_json_file(video_data):
    file_path = "/opt/airflow/data/data.json"
    with open(file_path, "w") as f:
        json.dump(video_data, f)

with DAG(
    dag_id="youtube_pipeline_extraction",
    start_date=datetime(2026, 9, 16),
    schedule="@hourly",
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_details",
        python_callable=extract_videos.extract
    )

    generate_json_task = PythonOperator(
        task_id="generate_json",
        python_callable=generate_json_file,
        op_args=[extract_task.output]
    )

    trigger_dag_2 = TriggerDagRunOperator(
        task_id="trigger_dw_update",
        trigger_dag_id="youtube_warehouse_pipeline"
    )

    extract_task >> generate_json_task >> trigger_dag_2

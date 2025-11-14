from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## Define our task

def preprocess_data():
    print("Preprocessing data...")

def train_model():
    print("Training model...")

def evaluate_model():
    print("Evaluating model...")

## Define the DAG
with DAG(
    "mlpipeline",
    schedule="@weekly",
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    preprocess_data_task = PythonOperator(
        task_id="preprocess_data",
        python_callable=preprocess_data,
    )

    train_model_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
    )

    evaluate_model_task = PythonOperator(
        task_id="evaluate_model",
        python_callable=evaluate_model,
    )

    # Define dependencies (Order matters)
    preprocess_data_task >> train_model_task >> evaluate_model_task
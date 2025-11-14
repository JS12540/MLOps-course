from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define functions for each task
def start_number(**context):
    context["ti"].xcom_push(key="current_value", value=10)
    return 10

def add_five(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="start_number_task")
    new_value = current_value + 5
    context["ti"].xcom_push(key="current_value", value=new_value)
    return new_value

def multiply_two(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="add_five_task")
    new_value = current_value * 2
    context["ti"].xcom_push(key="current_value", value=new_value)
    return new_value

def subtract_three(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="multiply_two_task")
    new_value = current_value - 3
    context["ti"].xcom_push(key="current_value", value=new_value)
    return new_value

def square(**context):
    current_value = context["ti"].xcom_pull(key="current_value", task_ids="subtract_three_task")
    new_value = current_value ** 2
    context["ti"].xcom_push(key="current_value", value=new_value)
    return new_value

# Define the DAG
with DAG(
    dag_id="maths_operations",
    schedule="@once",
    start_date=datetime(2022, 1, 1),
    catchup=False,
) as dag:

    start_number_task = PythonOperator(
        task_id="start_number_task",
        python_callable=start_number
    )

    add_five_task = PythonOperator(
        task_id="add_five_task",
        python_callable=add_five
    )

    multiply_two_task = PythonOperator(
        task_id="multiply_two_task",
        python_callable=multiply_two
    )

    subtract_three_task = PythonOperator(
        task_id="subtract_three_task",
        python_callable=subtract_three
    )

    square_task = PythonOperator(
        task_id="square_task",
        python_callable=square
    )

    # Set task dependencies
    start_number_task >> add_five_task >> multiply_two_task >> subtract_three_task >> square_task

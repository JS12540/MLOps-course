from airflow import DAG
from airflow.decorators import task
from datetime import datetime

# Define DAG
with DAG(
    dag_id="task_flow_api",
    schedule="@once",
    start_date=datetime(2022, 1, 1),
    catchup=False,
) as dag:

    @task
    def start_number():
        return 10

    @task
    def add_five(number):
        return number + 5

    @task
    def multiply_two(number):
        return number * 2

    @task
    def subtract_three(number):
        return number - 3

    @task
    def square(number):
        return number ** 2

    # Define the flow
    result = start_number()
    result = add_five(result)
    result = multiply_two(result)
    result = subtract_three(result)
    result = square(result)

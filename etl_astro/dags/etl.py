from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests

API_KEY = "7BbRvxo8uuzas9U3ho1RwHQQCkZIZtJojRIr293q"

with DAG(
    dag_id='nasa_apod_postgres',
    start_date=datetime.now() - timedelta(days=1),
    schedule='@daily',
    catchup=False
) as dag:

    @task
    def create_table():
        postgres = PostgresHook(postgres_conn_id="my_postgres_connection")
        postgres.run("""
            CREATE TABLE IF NOT EXISTS apod_data (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url TEXT,
                date DATE,
                media_type VARCHAR(50)
            );
        """)

    @task
    def extract_apod():
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
        response = requests.get(url)
        return response.json()

    @task
    def transform_apod_data(response):
        return {
            "title": response.get("title", ""),
            "explanation": response.get("explanation", ""),
            "url": response.get("url", ""),
            "date": response.get("date", ""),
            "media_type": response.get("media_type", "")
        }

    @task
    def load_data_to_postgres(apod):
        postgres = PostgresHook(postgres_conn_id="my_postgres_connection")
        postgres.run(
            """
            INSERT INTO apod_data (title, explanation, url, date, media_type)
            VALUES (%s, %s, %s, %s, %s);
            """,
            parameters=(
                apod["title"],
                apod["explanation"],
                apod["url"],
                apod["date"],
                apod["media_type"]
            )
        )

    create_table() >> load_data_to_postgres(transform_apod_data(extract_apod()))

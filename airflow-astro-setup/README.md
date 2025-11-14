Overview
========

Welcome to Astronomer! This project was generated after you ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache Airflow on your local machine.

Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes one example DAG:
    - `example_astronauts`: This DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this DAG works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

Start Airflow on your local machine by running 'astro dev start'.

This command will spin up five Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- DAG Processor: The Airflow component responsible for parsing DAGs
- API Server: The Airflow component responsible for serving the Airflow UI and API
- Triggerer: The Airflow component responsible for triggering deferred tasks

When all five containers are ready the command will open the browser to the Airflow UI at http://localhost:8080/. You should also be able to access your Postgres Database at 'localhost:5432/postgres' with username 'postgres' and password 'postgres'.

Note: If you already have either of the above ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.


###

# 🚀 Astronaut ETL Example – Airflow DAG

This project contains an **Apache Airflow DAG** that fetches the list of astronauts currently in space and prints details about each astronaut using **dynamic task mapping**.

## 📌 Overview

The DAG performs the following steps:

1. **Fetch astronaut data** from the Open Notify API
2. **Fallback to hardcoded data** if the API is unavailable
3. **Store metadata** (like number of astronauts) using XCom
4. **Use dynamic task mapping** to create one task per astronaut
5. **Print each astronaut's name and spacecraft**

This example demonstrates:

- Airflow **TaskFlow API**
- **Dynamic task mapping**
- Using **Assets**
- External API calls
- Clean, simple Python-based ETL with Airflow

---

## 🗂️ Files Included

| File | Description |
|------|-------------|
| `example_astronauts.py` | Main Airflow DAG |

---

## 📅 DAG Details

- **DAG ID:** `example_astronauts`
- **Schedule:** Runs every day (`@daily`)
- **Retry Policy:** Retries failed tasks up to 3 times
- **Start Date:** `2025-04-22`
- **Tags:** `example`

---

## 📦 Dependencies

This DAG requires:

- Python 3.10+
- Apache Airflow 2.9+
- `requests` package
- `pendulum` package

Install requirements:
```bash
pip install apache-airflow requests pendulum
```

If using Astronomer (Astro CLI), these dependencies will be automatically handled using your environment.

---

## 🧠 How the DAG Works

### 1️⃣ Task: `get_astronauts`

- Calls API: `http://api.open-notify.org/astros.json`
- Extracts:
  - Number of astronauts in space
  - List of astronauts (`name`, `craft`)
- Pushes number of astronauts to XCom
- Returns the list of astronauts
- Sets an Asset named `current_astronauts`

### 2️⃣ Task: `print_astronaut_craft`

- Receives:
  - A greeting (`"Hello! :)"`)
  - One astronaut dictionary (`{"name": "...", "craft": "..."}`)
- Prints the message:
```
{astronaut_name} is currently in space flying on the {craft}! Hello! :)
```

### 3️⃣ Dynamic Task Mapping

For each astronaut in the list returned by `get_astronauts()`, Airflow dynamically generates a task instance:
```
print_astronaut_craft[0]
print_astronaut_craft[1]
print_astronaut_craft[2]
...
```

The number of tasks changes depending on the number of astronauts.

---

## 🧩 DAG Flow Diagram
```
get_astronauts
       |
       ↓
print_astronaut_craft[astronaut #1]
print_astronaut_craft[astronaut #2]
print_astronaut_craft[astronaut #3]
...
```

---

## 🛠️ Running the DAG

If using Astronomer (`astro dev`):

1. Place this file inside the `dags/` directory
2. Start Airflow:
```bash
astro dev start
```

3. Visit Airflow UI:
```
http://localhost:8080
```

4. Enable the DAG named "example_astronauts"
5. Trigger it manually or wait for the daily schedule

---

## 📚 Useful Links

- [Airflow TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [Dynamic Task Mapping](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dynamic-task-mapping.html)
- [Astronomer Get Started Guide](https://www.astronomer.io/docs/learn/get-started-with-airflow)
- [Open Notify Astronaut API](http://api.open-notify.org/astros.json)
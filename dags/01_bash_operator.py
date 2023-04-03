# Licensed to the Apache Software Foundation (ASF)
# http://www.apache.org/licenses/LICENSE-2.0
"""
Example DAG: Bash Operator
"""
from __future__ import annotations

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


# DAG Definition
with DAG(
    "01_bash_operator",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple bash operator DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["01_bash_operator"],
) as dag:
    # dag documentation
    dag.doc_md = """
    This is DAGs documentation placed anywhere as string
    """

    # Tasks definition
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="echo 'Starting to Sleep zzz' && sleep 5 && echo 'wake up!'",
        retries=3,
    )

    # Task execution
    t1 >> t2

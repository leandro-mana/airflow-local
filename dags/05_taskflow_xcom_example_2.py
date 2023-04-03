# Licensed to the Apache Software Foundation (ASF)
# http://www.apache.org/licenses/LICENSE-2.0
"""
This DAG is demonstrating an Xcom to pass data between tasks by using TaskFlow API
"""
from __future__ import annotations

import requests
import json
from airflow.decorators import dag, task
from pendulum import datetime


URL = "http://catfact.ninja/fact"
DEFAULT_ARGS = {"start_date": datetime(2021, 1, 1), "retries": 2}


@dag(
    schedule="@daily",
    default_args=DEFAULT_ARGS,
    catchup=False,
    tags=["taskflow_xcom_example_1"],
)
def taskflow_xcom_example_2() -> None:
    @task
    def get_a_cat_fact() -> dict[str, str]:
        """
        Gets a cat fact from the CatFacts API
        """
        res = requests.get(URL)
        return {"cat_fact": json.loads(res.text)["fact"]}

    @task
    def print_the_cat_fact(cat_fact: dict[str, str]) -> None:
        """
        Prints the cat fact
        """
        print("Cat fact for today:", cat_fact.get("cat_fact", None))

    # Flow
    print_the_cat_fact(get_a_cat_fact())


taskflow_xcom_example_2()

# Licensed to the Apache Software Foundation (ASF)
# http://www.apache.org/licenses/LICENSE-2.0
"""
This DAG is demonstrating an Xcom to pass data between tasks by using TaskFlow API
"""
from __future__ import annotations

import logging
import requests
from datetime import datetime
from typing import Dict
from airflow.decorators import dag, task


DEFAULT_ARGS = {"start_date": datetime(2021, 1, 1), "retries": 2}
API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd\
    &include_market_cap=true&include_24hr_vol=true&include_24hr_change=true\
    &include_last_updated_at=true"


@dag(
    schedule="@daily",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2021, 12, 1),
    catchup=False,
    tags=["taskflow_xcom_example_1"],
)
def taskflow_xcom_example_1() -> None:
    """ """

    @task(task_id="extract", retries=2)
    def extract_bitcoin_price() -> Dict[str, str]:
        return requests.get(API).json()["bitcoin"]

    @task(multiple_outputs=True)
    def process_data(response: Dict[str, str]) -> Dict[str, str]:
        logging.info(response)
        return {"usd": response["last_updated_at"], "change": "usd_24h_change"}

    @task
    def store_data(data: Dict[str, str]):
        logging.info(f"Store: {data['usd']} with change {data['change']}")

    store_data(process_data(extract_bitcoin_price()))


taskflow_xcom_example_1()

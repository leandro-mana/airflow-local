# Licensed to the Apache Software Foundation (ASF)
# http://www.apache.org/licenses/LICENSE-2.0
"""
This DAG is demonstrating an Extract -> Transform -> Load pipeline
"""
from __future__ import annotations

import logging
import json
import pendulum
from airflow import DAG
from airflow.decorators import task


# Globals
LOG = logging.getLogger(__name__)


with DAG(
    "03_pyhon_operator_xcom",
    default_args={"retries": 2},
    description="DAG Python Operator Tutorial",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["03_pyhon_operator_xcom_example"],
) as dag:
    dag.doc_md = __doc__

    @task(task_id="extract")
    def extract(**kwargs):
        """
        A simple Extract task to get data ready for the rest of the data pipeline.
        In this case, getting data is simulated by reading from a hardcoded JSON string.
        This data is then put into xcom, so that it can be processed by the next task.
        """
        LOG.info("Starting extract")
        task_instance = kwargs["ti"]
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        task_instance.xcom_push("order_data", data_string)

    @task(task_id="transform")
    def transform(**kwargs):
        """
        A simple Transform task which takes in the collection of order data from xcom
        and computes the total order value.
        This computed value is then put into xcom, so that it can be processed by the next task.
        """
        LOG.info("Starting transform")
        task_instance = kwargs["ti"]
        extract_data_string = task_instance.xcom_pull(
            task_ids="extract", key="order_data"
        )
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        total_value = {"total_order_value": total_order_value}
        total_value_json_string = json.dumps(total_value)
        task_instance.xcom_push("total_order_value", total_value_json_string)

    @task(task_id="load")
    def load(**kwargs):
        """
        A simple Load task which takes in the result of the Transform task, by reading it
        from xcom and instead of saving it to end user review, just prints it out.
        """
        LOG.info("Starting load")
        task_instance = kwargs["ti"]
        total_value_string = task_instance.xcom_pull(
            task_ids="transform", key="total_order_value"
        )
        total_order_value = json.loads(total_value_string)

        LOG.info(
            "Total Order Value: %s", total_order_value.get("total_order_value", None)
        )
        LOG.info("ETL Finished")

    # Tasks
    extract_task = extract()
    transform_task = transform()
    load_task = load()

    # Flow
    extract_task >> transform_task >> load_task

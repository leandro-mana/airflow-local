# Licensed to the Apache Software Foundation (ASF)
# http://www.apache.org/licenses/LICENSE-2.0
"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions,
natively and within a virtual environment.
"""
from __future__ import annotations

import logging
import pendulum
from pprint import pprint
from airflow import DAG
from airflow.decorators import task


# Globals
LOG = logging.getLogger(__name__)

# DAG Definition
with DAG(
    dag_id="02_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    default_args={"retries": 2},
    tags=["02_python_operator_example"],
) as dag:

    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs) -> None:
        """Print the Airflow context and ds variable from the context."""
        pprint(kwargs)
        print(ds)

        LOG.info("Finished print_context()")
        return

    print_context_task = print_context()

    @task.virtualenv(
        task_id="virtualenv_python",
        requirements=["colorama==0.4.0"],
        system_site_packages=False,
    )
    def callable_virtualenv() -> None:
        """
        Example function that will be performed in a virtual environment with an explicit
        library required.

        Importing at the module level ensures that it will not attempt to import the
        library before it is installed.
        """
        import logging
        from time import sleep
        from colorama import Back, Fore, Style

        log = logging.getLogger(__name__)

        print(Fore.RED + "some red text")
        print(Back.GREEN + "and with a green background")
        print(Style.DIM + "and in dim text")
        print(Style.RESET_ALL)
        for _ in range(4):
            print(Style.DIM + "Please wait...", flush=True)
            sleep(1)

        log.info("Finished callable_virtualenv()")

    virtualenv_task = callable_virtualenv()

    # Order of execution
    print_context_task >> virtualenv_task

## Local Airflow Example

The purpose of this repo is to setup a local [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/) based on [docker-compose](https://docs.docker.com/compose/)

### Requirements
- [Python](https://docs.python-guide.org/starting/installation/)
- [Pipenv](https://docs.python-guide.org/dev/virtualenvs/)
- [Docker](https://docs.docker.com/get-docker/)
- [Make](https://www.gnu.org/software/make/)
- Optional - [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) - for running pytest via `make astro`

### Make

Run `make` for the help message, or follow below flow for an end to end run

```Bash
# Create Python Virtual environment via pipenv and install Airflow library
make pipenv
make airflow

# Run Black, Flake8 and MyPy in non-strict mode
make lint

# Optional - to run pytest via Astro CLI
# This method is preferred as does not require a running Airflow to run tests 
make astro

# Get all related Docker images for Airflow Local Run
make init

# Run Airflow Locally
# NOTE:
#   - URL: http://localhost:8080
#   - user/pass: airflow/airflow
#   - Once logged in, activate all the DAGs
make up

# Clean stopped containers
make down

# Clean stopped containers, volumes and Docker images
make clean
```

### Helpers

```Bash
# Locate Virtual Environment, use that PATH for IDE Python interpreter
pipenv --venv

# Remove Docker Dangling Images
docker rmi -f $(docker images -f "dangling=true" -q)

# Update Pipfile with new packages
pipenv install <package>
```


### **NOTES:**
- [Supported Installation](https://airflow.apache.org/docs/apache-airflow/2.4.3/installation/installing-from-pypi.html)
- Original Docker Compose [file](https://airflow.apache.org/docs/apache-airflow/2.4.3/docker-compose.yaml)
- Pipenv [cheat sheet]https://upengareri.github.io/pipenv_cheatsheet/
- Airflow [blogs](https://towardsdatascience.com/tagged/airflow)
- Airflow example [DAGs](https://github.com/apache/airflow/tree/main/airflow/example_dags)
- AWS, Amazon Managed Workflows for Apache Airflow [MWAA](https://www.youtube.com/watch?v=ZET50M20hkU&ab_channel=AmazonWebServices)
- [Astronomer Docs](https://docs.astronomer.io/)
- `from __future__ import annotations` [Why?](https://docs.python.org/3/library/__future__.html)
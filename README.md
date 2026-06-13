# jenkins-python-public

A small FastAPI application used in a Jenkins CI/CD workshop.
The goal is to walk through the full cycle: **clone from Git -> install -> lint -> test -> build artifact -> deploy**.

## What's in here

```
app/
  logic.py      # pure business logic (calculate_gross) - unit tested
  main.py       # FastAPI app (/, /health, /vat) - API tested
tests/
  test_logic.py # unit tests
  test_api.py   # HTTP tests (TestClient)
requirements.txt          # CI tooling: pytest, httpx, ruff, build
pyproject.toml            # runtime deps + ruff/pytest config + wheel build
Dockerfile                # production image of the app
Jenkinsfile               # CI/CD pipeline as code (Jenkins)
.github/workflows/ci.yml  # the same pipeline in GitHub Actions (for comparison)
```

## Run locally (without Jenkins)

```bash
python3 -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install . -r requirements.txt

ruff check .                  # lint
pytest --junitxml=report.xml  # tests + JUnit report
python -m build --wheel       # build the artifact (dist/*.whl)

uvicorn app.main:app --reload # run the app -> http://127.0.0.1:8000/docs
```

## Run as a container

```bash
docker build -t python-ci-demo .
docker run --rm -p 8000:8000 python-ci-demo
# check: http://127.0.0.1:8000/health
```

## Jenkins

The `Jenkinsfile` defines the full pipeline (install -> lint -> test -> build -> deploy/smoke).
Create a **Pipeline** job, choose **"Pipeline script from SCM"**, and point it at this repository
(branch `main`, Script Path `Jenkinsfile`). Jenkins checks out the repo and runs every stage.

## GitHub Actions

`.github/workflows/ci.yml` runs the same cycle (lint -> test -> build -> deploy/smoke) as a
GitHub Actions workflow. It triggers automatically on every push to `main` and on pull requests,
and tests the code across Python 3.11, 3.12 and 3.13. Same idea as the Jenkinsfile, expressed in
a different tool - handy for comparison.

## Note for real projects

In production, dependencies are usually **pinned exactly** (a lockfile: `uv`, `pip-tools`, or
`requirements.lock`) and split into runtime/dev. This repo uses loose version ranges so the
workshop keeps working regardless of when it is run.
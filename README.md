# GitHub Copilot Workshop

This is the work repository for Github Copilot Workshop in Github Universe Recap 2025, Jakarta, Indonesia.

## About

We are going to create Pomodoro web application using Python, JavaScript, HTML, and CSS.

## Getting started with `uv` and `venv`

### Dependencies

Install dependencies for the Pomodoro web app.

```bash
uv pip install flask flask-socketio
```

### venv
Install `venv` to create a virtual environment for this work project:
```bash
# install venv
uv venv
```

Activate `venv`:
```bash
# activate venv
source .venv/bin/activate
```

## Running Unit Tests

Unit tests are located in the `tests/` directory. To run all unit tests, make sure your virtual environment is activated:

```bash
source .venv/bin/activate
pytest
```

To see a coverage report:

```bash
pytest --cov
```

You can also run a specific test file:

```bash
pytest tests/test_timer_service.py
```

All test files use `pytest` and cover the main logic in models, services, routes, and config.

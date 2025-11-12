# GitHub Copilot Workshop

This is the work repository for Github Copilot Workshop in Github Universe Recap 2025, Jakarta, Indonesia.

## About

We are going to create Pomodoro web application using Python, JavaScript, HTML, and CSS.

## 🚀 Choose Your Version

This repository contains **two versions** of the Pomodoro Timer app:

### 1. 📦 Simple Version (Recommended for Easy Deployment)
**Single-file application** - Perfect for quick deployment and learning!

- ✅ **One file**: `simple_app.py` (all code in one place)
- ✅ **Minimal dependencies**: Only Flask required
- ✅ **Easy deploy**: Works on Heroku, Railway, Render, Docker, etc.
- ✅ **All features**: Full Pomodoro functionality maintained

👉 **[Read Simple Version Docs](README-simple.md)** | **[Deployment Guide](DEPLOYMENT.md)**

```bash
# Quick start with simple version
pip install flask
python simple_app.py
```

### 2. 🏗️ Full-Featured Version (Learning Architecture)
**Multi-module architecture** - Great for learning software design patterns!

- 📁 Modular structure (models, services, routes)
- 🔌 Real-time updates with Flask-SocketIO
- 🎨 Advanced UI with visual effects
- 📚 Educational architecture documentation

Continue reading below for the full-featured version setup...

## Getting started with Full-Featured Version

### Using `uv` and `venv`

### Dependencies

Install dependencies for the full-featured Pomodoro web app.

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

### Run the full-featured app

```bash
source .venv/bin/activate
python app.py
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

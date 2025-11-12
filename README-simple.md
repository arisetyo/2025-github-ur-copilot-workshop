# Simple Pomodoro Timer

A simplified, easy-to-deploy Pomodoro timer web application in a single Python file.

## Features

- 25-minute work sessions
- 5-minute short breaks
- 15-minute long breaks (after 4 work sessions)
- Clean, responsive UI
- Browser notifications
- Simple REST API
- Single file deployment

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-simple.txt
```

### Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the application
python simple_app.py
```

The application will be available at `http://localhost:5000`

## Deployment

### Deploy to Heroku

1. Create a `Procfile`:
```
web: python simple_app.py
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Deploy to PythonAnywhere

1. Upload `simple_app.py` and `requirements-simple.txt`
2. Create a new web app with Flask
3. Set the WSGI file to import from `simple_app`
4. Install requirements: `pip install -r requirements-simple.txt`

### Deploy to Railway/Render

1. Connect your GitHub repository
2. Set start command: `python simple_app.py`
3. The platform will auto-detect Flask and deploy

### Deploy with Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements-simple.txt .
RUN pip install -r requirements-simple.txt
COPY simple_app.py .
EXPOSE 5000
CMD ["python", "simple_app.py"]
```

Build and run:
```bash
docker build -t pomodoro-timer .
docker run -p 5000:5000 pomodoro-timer
```

## API Endpoints

- `GET /` - Main application page
- `GET /api/status` - Get current timer status
- `POST /api/start` - Start the timer
- `POST /api/pause` - Pause the timer
- `POST /api/reset` - Reset the timer
- `POST /api/skip` - Skip to next session
- `GET /health` - Health check endpoint

## Differences from Original

This simplified version removes:
- Flask-SocketIO (replaced with simple AJAX polling)
- Separate model/service/route files (all in one file)
- Complex configuration system
- Separate static files (CSS/JS embedded in HTML)
- Visual effects and animations
- Database dependencies

Benefits:
- ✅ Single file - easy to understand and modify
- ✅ Minimal dependencies - only Flask required
- ✅ Simple deployment - works on any Python hosting
- ✅ No WebSocket complexity - simpler infrastructure
- ✅ Fast startup - no module loading overhead

## License

MIT

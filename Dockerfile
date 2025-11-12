FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements-simple.txt .
RUN pip install --no-cache-dir -r requirements-simple.txt

# Copy application file
COPY simple_app.py .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=simple_app.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "simple_app.py"]

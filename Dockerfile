# Python base image
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the service
CMD ["python", "main.py"]

# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies and Python dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose port 8000 (if needed, for example, if you're running a web server)
EXPOSE 8000

# Set environment variables (example for OpenAI API key)
ENV OPENAI_API_KEY="your_openai_api_key_here"

# Define the command to run your application (entry point)
CMD ["python", "main.py"]

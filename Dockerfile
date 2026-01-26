FROM python:3.11-slim

# Install system dependencies including Octave
RUN apt-get update && apt-get install -y \
    octave \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pandas \
    numpy \
    matplotlib

# Copy the application files
COPY main.py validators.py index.html tasks.json /app/

# Expose the application port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

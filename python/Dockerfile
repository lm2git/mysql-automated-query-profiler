FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files
COPY requirements.txt .
COPY run_queries.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command (example)
CMD ["python", "run_queries.py"]

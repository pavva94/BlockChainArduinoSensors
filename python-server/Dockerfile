# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libbluetooth-dev \
    build-essential \
    bluez \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY requirements.txt /app
COPY http_server.py /app
COPY testWeb3.py /app
COPY testIPFS.py /app
COPY SensorData_abi.json /app

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required ports
EXPOSE 5002 8000 8545

# Run the Python server script
# for Arduino BLE connection
# CMD ["python", "server.py"]
# for FastAPI connection
CMD ["python", "http_server.py"]

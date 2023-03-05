# Use the official Python image as the base image
FROM python

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the working directory
COPY sensorloader.py .

# Run the Python script
CMD ["python", "sensorloader.py"]

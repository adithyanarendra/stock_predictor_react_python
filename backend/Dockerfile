# Use official Python image as a base
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the entire content of the current directory to /app
COPY . /app

# Install the required dependencies
RUN pip install -r requirements.txt

# Set the default command to run the app
CMD ["python", "app/main.py"]

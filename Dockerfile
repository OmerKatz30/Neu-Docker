# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY app_requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r app_requirements.txt

# Copy the application code into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run gunicorn to serve the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
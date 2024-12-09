# Start with a lightweight base image
FROM python:3.12.6-slim

# Set the working directory inside the container
WORKDIR /app
COPY requirements.txt /app/
# Copy a basic script to the container
RUN pip install -r /app/requirements.txt

# Run the application when the container starts
CMD ["python", "/app/app.py"]

# Use the official Python base image
FROM python:3.12-alpine

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    gfortran \
    libgfortran \
    openblas-dev \
    lapack-dev
# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

#RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that your application will be running on
EXPOSE 5303
EXPOSE 7860

# Start the application
CMD ["python", "app.py"]
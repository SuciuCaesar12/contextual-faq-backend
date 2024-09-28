# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# RUN yum install gcc -y

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the src/ directory into the container
COPY ./src /app/src

# Expose the port that FastAPI will run on
EXPOSE 80

# Command to run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

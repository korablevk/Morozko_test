FROM python:3.11-slim

# Set working directory
WORKDIR /images_microservice

# Copy requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Specify the default command
CMD ["uvicorn", "images_microservice.main:app", "--host", "0.0.0.0", "--port", "8000"]

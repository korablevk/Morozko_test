FROM python:3.11-slim

WORKDIR /images_microservice

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "images_microservice.main:app", "--host", "0.0.0.0", "--port", "7777"]

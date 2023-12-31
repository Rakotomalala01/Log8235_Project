FROM python:3.8-slim

WORKDIR /home/ubuntu

COPY app_8080.py .
COPY app_8081.py .
COPY requirements_container.txt .

RUN pip install -r requirements_container.txt


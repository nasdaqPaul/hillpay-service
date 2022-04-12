# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app .
WORKDIR /
CMD ["uvicorn","app:api", "--host=0.0.0.0"]
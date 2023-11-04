FROM python:3.10-slim

EXPOSE 8080

ENV HOME /small_flask

WORKDIR $HOME

COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt

ENV DB_HOST="localhost"
ENV DB_PORT="6379"

COPY . .



CMD gunicorn -b 0.0.0.0:8080 main:app
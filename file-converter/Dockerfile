
FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8
# Set environment varibles

COPY ./app /app

WORKDIR /app

RUN apk add ocrmypdf

RUN pip3 install -r requirements.txt

# RUN uvicorn main:app --port 8053
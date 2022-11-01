FROM python:3.8.10-alpine as base

RUN apk update && apk add gcc g++
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


FROM base as api

COPY api_service api_service
EXPOSE 5000

WORKDIR api_service
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


FROM base as stock

COPY stock_service stock_service
EXPOSE 5001

WORKDIR stock_service
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

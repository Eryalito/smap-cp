FROM python:3.11.0a3-alpine

RUN  apk add build-base && python -m pip install tinytuya pyyaml redis
WORKDIR /app
COPY *.py ./
ADD cache/ cache
ADD database/ database
ADD prices/ prices
ADD provider/ provider

ENTRYPOINT [ "python3", "main.py" ]
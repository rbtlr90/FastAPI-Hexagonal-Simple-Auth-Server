FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc postgresql

WORKDIR /sample-auth-server

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./ /sample-auth-server

CMD ["uvicorn", "app.main:app"]
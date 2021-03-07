FROM python:latest

RUN apt update && \
    apt install -y deluge-console

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD ./ /app

CMD python -u main.py

FROM python:2-alpine

ADD . /opt/lorumipse

WORKDIR /opt/lorumipse

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH .
EXPOSE 9999
CMD scripts/run-server.sh

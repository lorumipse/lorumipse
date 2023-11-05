FROM python:3-alpine

ADD . /opt/lorumipse

WORKDIR /opt/lorumipse

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH .
EXPOSE 9999
CMD scripts/run-server.sh

FROM ubuntu:15.10

RUN apt-get -y update && apt-get install -y python

ADD . /opt/lorumipse

WORKDIR /opt/lorumipse
ENV PYTHONPATH .
EXPOSE 9999
CMD scripts/run-server.sh

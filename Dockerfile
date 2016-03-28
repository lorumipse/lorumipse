FROM ubuntu:15.10

RUN apt-get -y update && apt-get install -y python && apt-get install -y python-pip
RUN pip install Flask
RUN pip install PyYAML
RUN pip install gunicorn

ADD . /opt/lorumipse

WORKDIR /opt/lorumipse
ENV PYTHONPATH .
EXPOSE 9999
CMD scripts/run-server.sh

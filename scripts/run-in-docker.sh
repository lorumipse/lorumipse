#!/bin/bash

if [ -z $DOCKER_HOST ]; then
    echo 'Docker environment is not defined. Connect to a docker machine e.g eval "$(docker-machine env default)"' 2>&1
	exit 1
fi

IMAGE=lorumipse

if ! docker images $IMAGE | grep $IMAGE; then
    echo "Image is not built yet, build it with docker build -t lorumipse ."
    exit 1
fi

docker run -d -p 80:9999 lorumipse
echo Use http://$(docker-machine ip):80/

#!/bin/bash

trap 'echo "Exiting"; exit 1' SIGINT SIGTERM

get_images() {
    echo "Collecting images"
    docker pull python:3.12-rc-slim-buster
}

docker_compose() {
    echo "Composing containers:"
    docker-compose up
}

get_images
docker_compose

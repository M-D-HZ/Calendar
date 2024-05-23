#! /bin/bash

trap 'echo "Exiting"; exit 1' SIGINT SIGTERM

get_images() {
    echo "Collecting images"
    podman pull python:3.12-rc-slim-buster
}

podman_compose() {
    echo "Composing containers:"
    podman compose up
}

get_images
podman_compose
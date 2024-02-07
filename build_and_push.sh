#!/bin/bash

source docker_credentials.txt

IMAGE_NAME="flask_portfolio"
TAG="latest"
CONTAINER_NAME="flask_portfolio"

# Create a Docker configuration file with credentials
echo "{\"auths\":{\"https://index.docker.io/v2/\":{\"auth\":\"$(echo -n $DOCKER_USERNAME:$DOCKER_PASSWORD | base64)\"}}}" > ~/.docker/config.json

# Docker login
#docker login --username $DOCKER_USERNAME --password-stdin < ~/.docker/config.json

# Remove password-file
rm ~/.docker/config.json

# Stop and remove the existing container
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

# Build Docker image
DOCKER_BUILDKIT=1 docker build -t zibax/$IMAGE_NAME:$TAG .

# Tag the image
docker tag $IMAGE_NAME:$TAG zibax/$IMAGE_NAME:$TAG

# Push to Docker.io
#docker push zibax/flask_portfolio:latest

# Run the new container
docker run -d --name $CONTAINER_NAME -p 5000:5000 zibax/$IMAGE_NAME:$TAG

# Save image to RPI
#docker save zibax/flask_portfolio:latest | ssh martin@rpi-ip 'docker load'

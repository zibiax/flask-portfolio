#!/bin/bash

source docker_credentials.txt

IMAGE_NAME="flask_portfolio"
TAG="latest"
CONTAINER_NAME="flask_portfolio"

# Create a Docker configuration file with credentials
# echo "{\"auths\":{\"https://index.docker.io/v2/\":{\"auth\":\"$(echo -n $DOCKER_USERNAME:$DOCKER_PASSWORD | base64)\"}}}" > ~/.docker/config.json

docker login
# docker login --username $DOCKER_USERNAME --password-stdin < ~/.docker/config.json

# Remove password-file
#rm ~/.docker/config.json

# Check if the container exists and stop it if it does
if docker ps -a --format '{{.Names}}' | grep -Eq "^$CONTAINER_NAME$"; then
    docker stop $CONTAINER_NAME
fi

# Check if the container exists and remove it if it does
if docker ps -a --format '{{.Names}}' | grep -Eq "^$CONTAINER_NAME$"; then
    docker rm $CONTAINER_NAME
fi

# Build Docker image
DOCKER_BUILDKIT=1 docker build -t zibax/$IMAGE_NAME:$TAG .
#docker build --no-cache -t zibax/$IMAGE_NAME:$TAG .

# Tag the image
docker tag $IMAGE_NAME:$TAG zibax/$IMAGE_NAME:$TAG

# Push to Docker.io
docker push zibax/flask_portfolio:latest

# Run the new container
docker run -d --name $CONTAINER_NAME -p 5000:5000 zibax/$IMAGE_NAME:$TAG

# Save image to RPI
#docker save zibax/flask_portfolio:latest | ssh martin@rpi-ip 'docker load'

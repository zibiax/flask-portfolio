#!/bin/bash

source docker_credentials.txt

IMAGE_NAME="flask_portfolio"
TAG="latest"
CONTAINER_NAME="flask_portfolio"

# Docker login
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

# Stop and remove the existing container
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

# Build Docker image
docker build -t zibax/$IMAGE_NAME:$TAG .

# Tag the image
docker tag $IMAGE_NAME:$TAG zibax/$IMAGE_NAME:$TAG

# Push to Docker.io
sudo docker push zibax/flask_portfolio:latest

# Run the new container
docker run -d --name $CONTAINER_NAME -p 5000:5000 zibax/$IMAGE_NAME:$TAG

# Save image to RPI
#docker save zibax/flask_portfolio:latest | ssh martin@rpi-ip 'docker load'

#!/bin/bash

# Build Docker image
docker build -t zibax/flask_portfolio:latest .

# Push to Docker.io
#sudo docker push zibiax.azurecr.io/blog_1:latest

# Save image to RPI
#docker save zibax/flask_portfolio:latest | ssh martin@rpi-ip 'docker load'

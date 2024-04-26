# Use an official Python runtime as a parent image
FROM continuumio/miniconda3:latest

# Set the working directory to /app
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . /app

# Install dependencies
RUN conda env create -f environment.yml

# Set environment variable
ENV SECRET_KEY=${SECRET_KEY}

# Activate the conda environment
SHELL ["conda", "run", "-n", "flask-portfolio", "/bin/bash", "-c"]

# Make port 80 the port used
EXPOSE 5000

# Run the Django development server
CMD ["conda", "run", "-n", "flask-portfolio", "flask", "run", "--host=0.0.0.0"]

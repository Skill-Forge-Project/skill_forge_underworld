# Base Python image
FROM python:3.12

# Image Labels. Update values for each build
LABEL Name="Skill-Forge Underworld"
LABEL Version="1.0.0"
LABEL Release="closed-beta"
LABEL ReleaseDate="25.10.2024"
LABEL Description="Skill Forge Underworld is a Flask microservice that provides a API for the Skill Forge Underworld Realm."
LABEL Maintainer="Aleksandar Karastoyanov <karastoqnov.alexadar@gmail.com>"
LABEL License="GNU GPL v3.0 license"
LABEL GitHub SourceCode="https://github.com/Skill-Forge-Project/skill_forge_underworld"

# Update the package list
RUN apt-get update
# RUN apt-get install build-essential libssl-dev libffi-dev python3-dev cargo -y

# Set default timezone
ENV TZ=Europe/Sofia
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \ 
    && dpkg-reconfigure -f noninteractive tzdata

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the Python app requirements
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install -r requirements.txt --no-cache --pre

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8000", "wsgi:app"]
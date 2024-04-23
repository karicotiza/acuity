# Pull Python Image
FROM python:3.12-bookworm
WORKDIR /app

# Install Python prod requirements
COPY requirements requirements
RUN rm requirements/dev.txt
RUN python3 -m pip install -r requirements/prod.txt

# Install FFmpeg
RUN apt update -y
RUN apt upgrade -y
RUN apt install ffmpeg -y

# Create folder for neural network
RUN mkdir /nn_model

# Copying source code
COPY . .
RUN rm Dockerfile
RUN rm .dockerignore

# Start command
ENTRYPOINT [ "bash", "init.sh" ]

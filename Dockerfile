# Use an official Python runtime as a parent image
FROM python:3.6.8

RUN groupadd -r beerblog && useradd -r -g beerblog beerblog

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install gcc
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# Install any needed packages
RUN cd /app && pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait && chmod +x ./start.sh

RUN mkdir -p /app/photo && chown -R beerblog:beerblog /app/photo

CMD ./start.sh

# Make port 8001 available to the world outside this container
EXPOSE 8001

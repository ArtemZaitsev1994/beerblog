# Use an official Python runtime as a parent image
FROM python:3.6.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN mv wait_docker_script /wait
RUN chmod +x /wait && chmod +x ./start.sh

# Install any needed packages
RUN cd /app && pip install -r requirements.txt

CMD ./start.sh

# Make port 9090 available to the world outside this container
EXPOSE 9090

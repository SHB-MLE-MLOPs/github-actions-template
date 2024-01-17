# command tu run this file : docker build -t image_name .
# command to run for create container with image built from this file : docker run -p 8001:8001 --name container_name image_name:latest
# command to run docker-compose : docker-compose up -d --build
# command to stop docker-compose : docker compose stop OR docker compose down OR docker compose kill
# command to restart docker-compose : docker compose restart

## Procedure to clean and restart of a Docker Instance
# Stop the container(s) using the following command : docker-compose down
# Delete all containers using the following command : docker rm -f $(docker ps -a -q)
# Delete all volumes using the following command : docker volume rm $(docker volume ls -q)
# Restart the containers using the following command : docker-compose up -d --build

# create the first layer of image. 
# Image layer will be sequential task (or command) we need to execute step by step in order to build our application  
# Use the official MySQL image from Docker Hub
FROM postgres:latest

# Create a user account within the Docker image which can be used to run processes or services within the container. 
#RUN \
#    adduser --disabled-password --gecos '' ml-api-user && \
#	adduser --disabled-password --gecos '' sbodjona

# Sets or specify the working directory for any subsequent RUN, CMD, COPY, and other filesystem-related commands. 
# WORKDIR /data_base/POSTGRESS/server/

# Create and activate a virtual environement
#RUN \
#    python -m venv venv /backend && \
#    /bin/bash -c "source venv/bin/activate"

# Set the environment variables for PostgreSQL
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
# ENV POSTGRES_DB=mydatabase

# Set or Specify to Docker the environement variable can be use by the application 
ENV SERVER_PORT=5432

# copy file ("myAppToRun.jar" here) or folder contents from host system into to container image in specified path
COPY ./server/ /data_base/POSTGRESS/server/

# Update and install pip, tox and dependancies
#RUN \
#    pip install --no-cache-dir --upgrade pip && \
#	pip install --no-cache-dir --upgrade tox && \
#	pip install --no-cache-dir -r /backend/api/titanic_survived_prediction_api/requirements/test_requirements.txt && \
#	pip install --no-cache-dir -i https://test.pypi.org/simple/ titanic-survived-prediction-kcamille==0.0.1


# Adding the execute permission to the script "run.sh". The Docker will have a permission to execute "run.sh" script. 
# the goal of "run.sh" is to run the API on uvicorn web server 
RUN chmod +x /data_base/POSTGRESS/server/run.sh

# Give the acces or permission for user and group "ml-api-user:ml-api-user",
# to be able to change the ownerships (porperties) of files and directories within the Docker image
# RUN chown -R ml-api-user:ml-api-user /data_base/POSTGRESS/server/

# Set or Specify the user ("ml-api-user") and/or user group ("ml-api-user") under which the subsequent or bellow commands should be executed.
# USER ml-api-user

# Set or Specify the user and group for subsequent commands
# USER myuser:mygroup

# Expose container created to be able to connect our local or other machine to container 
EXPOSE $SERVER_PORT

# Set the working directory to "/usr/sbodjona/src/api/titanic_survived_prediction_api" where "run.sh" file is
WORKDIR /data_base/POSTGRESS/server

# To specify the default command to run when a container is launched from the image built, and it can be overridden (replaced) when running the container from the command line
# ./ this means run the command in the working directory created with WORKDIR command
# CMD instruction to start MySQL server
# CMD ["bash", "./run.sh"]
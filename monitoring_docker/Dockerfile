# create the first layer of python image.
FROM python:3.11-slim

# Create a user account within the Docker image which can be used to run processes or services within the container. 
RUN \
    adduser --disabled-password --gecos '' ml-monitoring-user && \
	adduser --disabled-password --gecos '' sbodjona

# Sets or specify the working directory for any subsequent RUN, CMD, COPY, and other filesystem-related commands. 
WORKDIR /monitoring_docker

# Create and activate a virtual environement
RUN \
    python -m venv venv /monitoring_docker && \
    /bin/bash -c "source venv/bin/activate"

# Set or Specify to Docker the environement variable can be use by the application 
ENV APP_PORT=8501

# copy file ("myAppToRun.jar" here) or folder contents from host system into to container image in specified path
COPY ./monitoring/ /monitoring_docker/monitoring/

# Update and install pip, tox and dependancies
RUN \
    pip install --no-cache-dir --upgrade pip && \
	pip install --no-cache-dir --upgrade tox && \
	pip install --no-cache-dir -r /monitoring_docker/monitoring/requirements/test_requirements.txt

# Adding the execute permission to the script "run.sh". The Docker will have a permission to execute "run.sh" script. 
# the goal of "run.sh" is to run monitoring app
RUN chmod +x /monitoring_docker/monitoring/run.sh

# Give the acces or permission for user and group "ml-monitoring-user:ml-monitoring-user",
# to be able to change the ownerships (porperties) of files and directories within the Docker image
RUN chown -R ml-monitoring-user:ml-monitoring-user /monitoring_docker/monitoring/

# Set or Specify the user ("ml-monitoring-user") and/or user group ("ml-monitoring-user") under which the subsequent or bellow commands should be executed.
USER ml-monitoring-user

# Expose container created to be able to connect our local or other machine to container 
EXPOSE $APP_PORT 

# Set the working directory
WORKDIR /monitoring_docker/monitoring

# To specify the default command to run when a container is launched from the image built, and it can be overridden (replaced) when running the container from the command line
# ./ this means run the command in the working directory created with WORKDIR command
CMD ["bash", "./run.sh"]

# create the first layer of image using the official MySQL image from Docker Hub.
FROM mysql:latest

# Sets or specify the working directory for any subsequent RUN, CMD, COPY, and other filesystem-related commands. 
WORKDIR /data_base_docker

# Set the root password for MySQL (change it to a secure password)
ENV MYSQL_ROOT_PASSWORD=root_password

# Create a new database and user
ENV MYSQL_DATABASE=db_for_api_user
ENV MYSQL_USER=sbodjona
ENV MYSQL_PASSWORD=BUij44Nr1986

# Set the default character set and collation
ENV MYSQL_CHARSET=utf8mb4
ENV MYSQL_COLLATION=utf8mb4_unicode_ci

# Set or Specify to Docker the environement variable can be use by the application 
ENV SERVER_PORT=3306

# copy file ("myAppToRun.jar" here) or folder contents from host system into to container image in specified path
COPY ./server/ /data_base_docker/MySQL/apiuser/server/

# Adding the execute permission to the script "run.sh". The Docker will have a permission to execute "run.sh" script. 
# the goal of "run.sh" is to run mysql server 
RUN chmod +x /data_base_docker/MySQL/apiuser/server/run.sh

# Expose container created to be able to connect our local or other machine to container 
EXPOSE $SERVER_PORT

# Set the working directory
WORKDIR /data_base_docker/MySQL/apiuser/server

# To specify the default command to run when a container is launched from the image built, and it can be overridden (replaced) when running the container from the command line
# ./ this means run the command in the working directory created with WORKDIR command
# CMD instruction to start MySQL server
CMD ["bash", "./run.sh"]
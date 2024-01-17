# create the first layer of image using the official PHPMyAdmin image from Docker Hub. 
FROM phpmyadmin/phpmyadmin:latest

# Sets or specify the working directory for any subsequent RUN, CMD, COPY, and other filesystem-related commands. 
WORKDIR /graphic_interface_docker

# Set environment variables for PHPMyAdmin configuration
ENV PMA_ARBITRARY=1

# Set or Specify to Docker the environement variable can be use by the application 
ENV APP_PORT=80

# Expose container created to be able to connect our local or other machine to container 
EXPOSE $APP_PORT

# Set the working directory
WORKDIR /graphic_interface_docker/MySQL/phpmyadmin

# To specify the default command to run when a container is launched from the image built, and it can be overridden (replaced) when running the container from the command line
# ./ this means run the command in the working directory created with WORKDIR command
CMD ["bash", "./run.sh"]

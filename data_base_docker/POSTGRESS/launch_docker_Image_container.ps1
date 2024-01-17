# command to run this file : .\launch_docker_Image_container.ps1

# Build the PHPMyAdmin Docker image
docker build -t postgress_server_image .

# Run the PHPMyAdmin container
docker run -p 5432:5432 --name container_mysql_server -d postgress_server_image:latest
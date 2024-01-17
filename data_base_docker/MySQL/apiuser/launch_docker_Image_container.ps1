# command to run this file : .\launch_docker_Image_container.ps1

# Build the PHPMyAdmin Docker image
docker build -t mysql_server_image .

# Run the PHPMyAdmin container
docker run -p 8181:3306 --name mysql_server_container -d mysql_server_image:latest
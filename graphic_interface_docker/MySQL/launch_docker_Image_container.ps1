# command to run this file : .\launch_docker_Image_container.ps1

# Build the PHPMyAdmin Docker image
docker build -t phpmyadmin_image .

# Run the PHPMyAdmin container
docker run -p 8080:80 --name phpmyadmin_container -d phpmyadmin_image:latest
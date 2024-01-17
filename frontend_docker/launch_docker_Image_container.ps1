# command to run this file : .\launch_docker_Image_container.ps1

# Build the PHPMyAdmin Docker image
docker build -t frontend_app_image .

# Run the PHPMyAdmin container
docker run -p 8501:8501 --name frontend_app_container -d frontend_app_image:latest
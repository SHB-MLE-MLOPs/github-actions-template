# command to run this file : .\launch_docker_Image_container.ps1

# Build the api Docker image
docker build -t api_image .

# Run the api container
docker run -p 8001:8001 --name api_container -d api_image:latest
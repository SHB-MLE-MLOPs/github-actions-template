# command to run this file : .\clean_restart_docker_Instance.ps1

## Run the containers using docker-compose command :
docker-compose up -d --build
## Stop the container(s) using the following command :
# docker-compose down
## Delete all containers using the following command :
# command in terminal
# docker rm -f $(docker ps -a -q)
# command in Windows PowerShell file (.ps1)
# docker ps -a -q | ForEach-Object { docker stop $_ ; docker rm -f $_ }
## Delete all volumes using the following command : 
# command in terminal
# docker volume rm $(docker volume ls -q)
# command in Windows PowerShell file (.ps1)
# docker volume ls -q | ForEach-Object { docker volume rm $_ }
## Restart the containers using the following command :
# docker-compose up -d --build
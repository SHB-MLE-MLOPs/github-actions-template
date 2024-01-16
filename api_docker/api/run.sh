# "uvicorn" server will start serving the ASGI application "app" located in the specified module "app.main" on the specified host (0.0.0.0) and port (the value of the $PORT environment variable). 
# The application can be accessed through a web browser or by making HTTP requests to the server's IP address and port.
# Make sure that the ASGI application and any required dependencies are properly set up in your environment before running this command. 
# Additionally, you need to ensure that the $PORT environment variable is defined and has the correct port number for your application to listen on.
uvicorn building_fastapi_api.create_fastapi_api:api --host 0.0.0.0 --port $API_PORT
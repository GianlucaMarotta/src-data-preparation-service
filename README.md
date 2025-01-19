# SRC Data Preparation Service

## Overview
This project provides a FastAPI-based web service to prepare user data by either copying files or creating symbolic links. The service allows users to specify methods and target paths for file preparation.
This project is a personal prototype for demonstration purpose, it is not meant to be used in production and it is not official code of SRC project. 

## Features
- Validate local file paths.
- Create user-specific directories.
- Copy files or create symbolic links based on user requests.
- Error handling for invalid paths, unsupported methods, and existing files.

## Endpoints

### `POST /prepare-data`
**Description**: Prepares data by either copying files or creating symbolic links.

#### Request Body
```json
{
  "data": ["local-path-on-storage", "relative-path-in-user-area"],
  "parameters": {
    "method": "copy_files" | "create_symlink",
    "username": "string"
  }
}
```

- **data**: A tuple containing the local file path and the relative path in the user area.
- **parameters**:
  - `method`: The operation to perform (`copy_files` or `create_symlink`).
  - `username`: The name of the user for whom the data is being prepared.

#### Responses
- **200 OK**: Success response with the target path.
  ```json
  {
    "status": "success",
    "target_path": "string"
  }
  ```
- **400 Bad Request**: Errors such as invalid paths, unsupported methods, or existing target paths.
  ```json
  {
    "detail": "Error message"
  }
  ```
- **500 Internal Server Error**: Unexpected errors during processing.

- **422 Unprocessable Entity**: Mandatory values are missing in input
  ```json
  {
    "detail": [
        {
        "loc": ["body", "parameters"],
        "msg": "Parameters must include 'method' and 'username'",
        "type": "value_error"
        }
    ]
  }
  ```

## Installation

The dependencies of this project should be installed and set up using **Poetry**.

Poetry is a tool for managing Python dependencies and projects, and it simplifies the process of managing virtual environments.

If you haven't already installed Poetry, follow the instructions on the [Poetry installation page](https://python-poetry.org/docs/#installation).


### Install dependencies

Once Poetry is installed, navigate to the project directory and run the following command to install the project and its dependencies:
```
poetry install
```
This will create a virtual environment and install all required dependencies as defined in pyproject.toml.

To install on the system without creating the virtual enviroment:
```
poetry config virtualenvs.create false && poetry install
```

### Activate the virtual environment (optional)
Poetry manages virtual environments automatically. To activate the environment, use:
  ```
  poetry shell
  ```

  > **_NOTE:_**
  >`poetry shell` has been removed since poetry v2.0.0. use `poetry env activate` instead.

## Run tests

Unit tests are present in the folder `tests/unit`. After installing the project, to run them: 
```
pytest
```
To run a specific test: 
```
pytest -k <test_name>
```

## Example Usage

### Running the service

After installation, to run the FastAPI service:
```
uvicorn prepare_data_service:app --host <hostname> --port 8000 --reload
```

### Request

Request on the service can be sent via an HTTP client as curl 

```bash
curl -X POST "http://<hostname>:8000/prepare-data" \
-H "Content-Type: application/json" \
-d '{
  "data": ["/path/to/local/storage/", "relative/path/in/user/area/"],
  "parameters": {
    "method": "<method_name>",
    "username": "<user_name>"
  }
}'
```

or with the use of a simple python script, as the one in `tests/example/client.py`

## Containerization with Docker

This section explains how to containerize the data preparation service using Docker, ensuring portability and ease of deployment across different environments. 

If not installed please install Docker from Docker's official website

### Steps to Build and Run the Container

Follow these steps to build and run the Docker container for the service.

#### Build the Docker Image

The following command should be used to build the Docker image. This command installs dependencies using Poetry and sets up the service inside the container:
```
docker build -t prepare-data:0.1.0 .
```

#### Run the Docker Container

To start the container, run the following command:
```
docker run
  -p 8000:8000 \
  -v /path/to/localstorage:/app/localstorage \
  -v /path/to/user_areas:/app/user_areas \
  prepare-data:0.1.0
```
with this command, we are exposing the port 8000 to the host and mounting as volumes the localstorage and userareas

### Access the Service

Once the container is running, access the API by making requests to:

http://localhost:8000/process

Request can be sent with methods cited in the previous section. Be sure to use `localhost` as `<hostname>`.

NOTE: The paths in the request must be the ones of the running container and not the ones of the host (e.g. /app/localstorage and not /path/to/localstorage)

## Deploying in K8s (WIP)

This service will have its natural deployment in a cluster with kubernetes services running. Preliminary settings are present in the folder `k8s_files`. Having a k8s cluster active, or a `minikube` a namespace containing the service can be deployed with:
```
make deploy
```
to remove the namespace: 
```
make delete
```


## Project Structure
```
.
├── Dockerfile # Dockerfile for containerizing the application 
├── k8s_files # Kubernetes configuration files for deployment 
├── LICENSE # License file for the project 
├── Makefile # Automation script for common tasks  
├── poetry.lock # Poetry lock file to ensure consistent dependencies 
├── pyproject.toml # Poetry configuration file for project metadata and dependencies 
├── README.md # Project README file (this file)  
├── src # Source code for the application │  
├── tests # Unit tests ad examples to be run manually
```

## License
This project is licensed under the BSD-3-Clause License. See `LICENSE` for more details.

## Contact
For inquiries, please contact `gianlucamarotta18@gmail.com`.


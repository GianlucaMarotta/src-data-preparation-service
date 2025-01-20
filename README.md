# SRC Data Preparation Service

## Overview
This project provides a FastAPI-based web service for preparing user data by either copying files or creating symbolic links. Users can specify methods and target paths for file preparation.

**Note:** This project is a personal prototype intended for demonstration purposes only. It is not designed for production use and is not an official SRC project.

## Features
- Validation of local file paths.
- Creation of user-specific directories.
- File copying or symbolic link creation based on user requests.
- Error handling for invalid paths, unsupported methods, and existing files.

## Endpoints

### `POST /prepare-data`
**Description:** Prepares data by either copying files or creating symbolic links.

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
- **200 OK**: Successful operation with the target path.
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
- **500 Internal Server Error**: Unexpected processing errors.
- **422 Unprocessable Entity**: Missing mandatory input values.
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

Project dependencies should be installed and set up using **Poetry**, a dependency management tool for Python that simplifies virtual environment management.

If Poetry is not installed, follow the instructions on the [Poetry installation page](https://python-poetry.org/docs/#installation).

### Install dependencies

Once Poetry is installed, navigate to the project directory and run the following command to install the project and its dependencies:
```
poetry install
```
This command creates a virtual environment and installs all required dependencies as defined in `pyproject.toml`.

To install dependencies without creating a virtual environment:
```
poetry config virtualenvs.create false && poetry install
```

### Activate the virtual environment (optional)
Poetry manages virtual environments automatically. To activate the environment, use:
```
poetry shell
```
> **_NOTE:_**
> The command `poetry shell` has been deprecated since Poetry v2.0.0. Use `poetry env activate` instead.

## Running Tests

Unit tests are located in the `tests/unit` directory. After installing the project, run the tests with:
```
pytest
```
To run a specific test:
```
pytest -k <test_name>
```

## Example Usage

### Running the service

After installation, start the FastAPI service with:
```
uvicorn prepare_data_service:app --host <hostname> --port 8000 --reload
```

### Sending Requests

You can send requests using an HTTP client such as `curl`:
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
Alternatively, use the provided Python script located in `tests/example/client.py`.

## Containerization with Docker

This section explains how to containerize the data preparation service using Docker, ensuring portability and ease of deployment across different environments.

If Docker is not installed, download it from [Docker's official website](https://www.docker.com/get-started).

### Steps to Build and Run the Container

#### Build the Docker Image

To build the Docker image, use the following command:
```
docker build -t prepare-data:0.1.0 .
```

#### Run the Docker Container

To start the container, run:
```
docker run \
  -p 8000:8000 \
  -v /path/to/localstorage:/app/localstorage \
  -v /path/to/user_areas:/app/user_areas \
  prepare-data:0.1.0
```
This command exposes port 8000 to the host and mounts the `localstorage` and `user_areas` directories as volumes.

### Accessing the Service

Once the container is running, access the API at:

http://localhost:8000/process

Requests can be sent using the methods described earlier. Be sure to use `localhost` as the `<hostname>`.

**Note:** Paths specified in requests must match the container paths (e.g., `/app/localstorage` instead of `/path/to/localstorage`).

## Deployment in Kubernetes (WIP)

This service is intended to be deployed in a Kubernetes cluster. Preliminary configurations can be found in the `k8s_files` directory. If a Kubernetes cluster (or Minikube) is active, deploy the service with:
```
make deploy
```
To remove the deployment:
```
make delete
```

## Project Structure
```
.
├── Dockerfile          # Docker configuration for containerization
├── k8s_files           # Kubernetes deployment configurations
├── LICENSE             # License information
├── Makefile            # Automation script for common tasks
├── poetry.lock         # Dependency lock file
├── pyproject.toml       # Project metadata and dependencies
├── README.md            # Project documentation (this file)
├── src                  # Application source code
├── tests                # Unit tests and examples
```

## License
This project is licensed under the BSD-3-Clause License. See the `LICENSE` file for more details.

## Contact
For inquiries, please contact `gianlucamarotta18@gmail.com`.


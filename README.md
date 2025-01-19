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

## Running Tests

## Deploying in K8s

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

## Example Usage

### Request
```bash
curl -X POST "http://127.0.0.1:8000/prepare-data" \
-H "Content-Type: application/json" \
-d '{
  "data": ["/path/to/source/file.txt", "destination/file.txt"],
  "parameters": {
    "method": "copy_files",
    "username": "johndoe"
  }
}'
```

### Response
```json
{
  "status": "success",
  "target_path": "user_areas/johndoe/destination/file.txt"
}
```
## License
This project is licensed under the BSD-3-Clause License. See `LICENSE` for more details.

## Contact
For inquiries, please contact `gianlucamarotta18@gmail.com`.


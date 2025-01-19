import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from pathlib import Path
from src_data_preparation import app 

client = TestClient(app)

def test_prepare_data_copy_files_success():
    """
    Tests that the `/prepare-data` endpoint correctly copies a file
    when the `method` parameter is `"copy_files"`.

    Verifies that the target path is correctly constructed and that the
    `shutil.copy` function is called with the correct arguments.
    """
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.mkdir") as mock_mkdir, \
         patch("shutil.copytree") as mock_copy:
        
        input_json = {
            "data": ["/valid/local/path", "user_subpath/file.txt"],
            "parameters": {"method": "copy_files", "username": "testuser"},
        }
        response = client.post("/prepare-data", json=input_json)
        assert response.status_code == 200
        assert response.json() == {"status": "success", "target_path": "user_areas/testuser/user_subpath/file.txt"}
        mock_mkdir.assert_called_once()
        mock_copy.assert_called_once_with(Path("/valid/local/path"), Path("user_areas/testuser/user_subpath/file.txt"))


def test_prepare_data_symlink_success():
    """
    Tests that the `/prepare-data` endpoint correctly creates a symlink
    when the `method` parameter is `"create_symlink"`.

    Verifies that the target path is correctly constructed and that the
    `os.symlink` function is called with the correct arguments.
    """
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.mkdir") as mock_mkdir, \
         patch("os.symlink") as mock_symlink:
        
        input_json = {
            "data": ["/valid/local/path", "user_subpath/file.txt"],
            "parameters": {"method": "create_symlink", "username": "testuser"},
        }

        response = client.post("/prepare-data", json=input_json)
        assert response.status_code == 200
        assert response.json() == {"status": "success", "target_path": "user_areas/testuser/user_subpath/file.txt"}
        mock_mkdir.assert_called_once()
        mock_symlink.assert_called_once_with(Path("/valid/local/path"), Path("user_areas/testuser/user_subpath/file.txt"))


def test_prepare_data_invalid_method():
    """
    Tests that the `/prepare-data` endpoint returns a 400 status code when
    the `method` parameter is not one of the supported methods.

    Verifies that the response JSON includes the correct error message.
    """
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.mkdir") as mock_mkdir:
    
        input_json = {
            "data": ["/valid/local/path", "user_subpath/file.txt"],
            "parameters": {"method": "invalid_method", "username": "testuser"},
        }

        response = client.post("/prepare-data", json=input_json)
        print(f"stica {response}")
        assert response.status_code == 400
        assert response.json()["detail"] == "Unsupported method: invalid_method"


def test_prepare_data_local_path_not_exist():
    """
    Tests that the `/prepare-data` endpoint returns a 400 status code 
    and the appropriate error message when the local path does not exist.

    Verifies that the response JSON includes the "Local path does not exist." detail.
    """

    with patch("pathlib.Path.exists", return_value=False):
        
        input_json = {
            "data": ["/invalid/local/path", "user_subpath/file.txt"],
            "parameters": {"method": "copy_files", "username": "testuser"},
        }

        response = client.post("/prepare-data", json=input_json)
        assert response.status_code == 400
        assert response.json()["detail"] == "Local path does not exist."


def test_prepare_data_target_path_already_exists():
    
    """
    Tests that the `/prepare-data` endpoint returns a 400 status code 
    and the appropriate error message when the target path already exists.

    Verifies that the response JSON includes the "Target path already exists." detail.
    """
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.mkdir", side_effect=FileExistsError("Target path already exists.")):
        
        input_json = {
            "data": ["/valid/local/path", "user_subpath/file.txt"],
            "parameters": {"method": "copy_files", "username": "testuser"},
        }

        response = client.post("/prepare-data", json=input_json)
        assert response.status_code == 400
        assert response.json()["detail"] == "Target path already exists."


def test_prepare_data_parameters_missing():
    """
    Tests that the `/prepare-data` endpoint returns a 422 status code
    and the appropriate error message when the `parameters` dictionary
    is missing one of the required keys (either "method" or "username").

    Verifies that the response JSON includes a "parameters" key in the
    "loc" field of the error detail.
    """
    input_json = {
        "data": ["/valid/local/path", "user_subpath/file.txt"],
        "parameters": {"username": "testuser"},  # Missing "method"
    }

    response = client.post("/prepare-data", json=input_json)
    assert response.status_code == 422
    assert "parameters" in response.json()["detail"][0]["loc"]


def test_prepare_data_unexpected_error():
    """
    Tests that the `/prepare-data` endpoint returns a 500 status code
    and includes the original error message in the response JSON
    when an unexpected error occurs.

    Verifies that the response JSON includes the error message.
    """
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.mkdir", side_effect=Exception("Unexpected error")):
        
        input_json = {
            "data": ["/valid/local/path", "user_subpath/file.txt"],
            "parameters": {"method": "copy_files", "username": "testuser"},
        }

        response = client.post("/prepare-data", json=input_json)
        assert response.status_code == 500
        assert "Unexpected error" in response.json()["detail"]

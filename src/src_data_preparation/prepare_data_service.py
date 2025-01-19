from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import Tuple
import shutil
import os
from pathlib import Path
import logging

app = FastAPI()

logger = logging.getLogger(__name__)

class DataRequest(BaseModel):
    data: Tuple[str, str]  # (local-path-on-storage, relative-path-in-user-area)
    parameters: dict  # {"method": str, "username": str}

    @validator("parameters")
    def validate_parameters(cls, value):
        if "method" not in value or "username" not in value:
            raise ValueError("Parameters must include 'method' and 'username'")
        return value


@app.post("/prepare-data")
async def prepare_data(request: DataRequest):
    """
    Prepares data by either copying files or creating symbolic links.

    Args:
    request: DataRequest
        A DataRequest object containing the local path on storage, the relative
        path in the user area, the method to use (copy_files or create_symlink),
        and the username.

    Returns:
    dict: A dictionary with a "status" key set to "success" and a "target_path"
        key set to the path of the prepared data.

    Raises:
    HTTPException: If the local path does not exist, the target path already
        exists, or the method is unsupported.
    """

    try:
        local_path, relative_path = request.data
        method = request.parameters["method"]
        username = request.parameters["username"]

        # Validate paths
        local_path = Path(local_path)

        if not local_path.exists():
            raise HTTPException(status_code=400, detail="Local path does not exist.")
            
        user_area = Path(f"user_areas/{username}")
        target_path = user_area / relative_path

        user_area.mkdir(parents=True, exist_ok=True)
      
        if method == "copy_files":
            shutil.copytree(local_path, target_path)
        elif method == "create_symlink":
            os.symlink(local_path, target_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported method: {method}")

    except FileExistsError: 
            raise HTTPException(status_code=400, detail="Target path already exists.")

    except Exception as exc:
        logger.error(f"Error processing request: {str(exc)}")
        if type(exc) == HTTPException:
            raise exc
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(exc)}")     

    logger.info(f"Data prepared for user {username} with method {method}.")

    return {"status": "success", "target_path": str(target_path)}


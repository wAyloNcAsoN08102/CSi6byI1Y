# 代码生成时间: 2025-08-07 00:02:22
import os
import shutil
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json
from sanic_cors import CORS
import asyncio

# Define the application
app = Sanic("FileBackupSync")
CORS(app)

# Define constants for source and destination directories
SOURCE_DIR = "./source"
DESTINATION_DIR = "./destination"

# Ensure source and destination directories exist
if not os.path.exists(SOURCE_DIR):
    os.makedirs(SOURCE_DIR)
if not os.path.exists(DESTINATION_DIR):
    os.makedirs(DESTINATION_DIR)

async def backup_files(request: Request):
    """
    Backup files from source directory to destination directory
    
    Args:
        request (Request): A Sanic request object
    """
    try:
        # Get file list from source directory
        source_files = os.listdir(SOURCE_DIR)

        # Loop through each file in source directory
        for file_name in source_files:
            # Construct file path
            source_file_path = os.path.join(SOURCE_DIR, file_name)
            destination_file_path = os.path.join(DESTINATION_DIR, file_name)

            # Check if file exists in destination directory
            if not os.path.exists(destination_file_path):
                # Copy file from source to destination
                shutil.copy2(source_file_path, destination_file_path)
            else:
                # Update file if it exists in destination
                shutil.copy2(source_file_path, destination_file_path)

        # Return success message
        return json({
            "status": "success",
            "message": "Backup completed successfully"
        })
    except Exception as e:
        # Handle exceptions and return error message
        return json({
            "status": "error",
            "message": str(e)
        }, status=500)

@app.route("/backup", methods=["POST"])
async def backup_handler(request: Request):
    """
    Handle backup request
    
    Args:
        request (Request): A Sanic request object
    """
    return await backup_files(request)

if __name__ == "__main__":
    # Run the application
    app.run(host="0.0.0.0", port=8000)
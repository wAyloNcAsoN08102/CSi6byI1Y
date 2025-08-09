# 代码生成时间: 2025-08-09 10:50:16
import os
import glob
from sanic import Sanic, response
from sanic.request import Request

# Initialize Sanic application
app = Sanic('BatchRenameTool')

# Route to handle file renaming
@app.route('(rename/<folder:path>)', methods=['POST'])
async def rename_files(request: Request, folder: str):
    # Extract JSON payload from the request
    try:
        payload = request.json
    except ValueError:
        return response.json({'error': 'Invalid JSON payload'}, status=400)

    # Check if the required parameters are present in the payload
    if 'prefix' not in payload or 'suffix' not in payload:
        return response.json({'error': 'Missing required parameters'}, status=400)

    # Extract prefix and suffix from the payload
    prefix = payload['prefix']
    suffix = payload['suffix']

    # Get all files in the specified folder
    files = glob.glob(os.path.join(folder, '*'))

    # Initialize a counter for naming files
    file_index = 1

    try:
        # Loop through all files and rename them
        for file_path in files:
            if os.path.isfile(file_path):
                # Extract the file extension
                file_name, file_extension = os.path.splitext(file_path)
                # Construct the new file name
                new_file_name = f"{prefix}{file_index:03d}{suffix}{file_extension}"
                # Rename the file
                os.rename(file_path, os.path.join(folder, new_file_name))
                file_index += 1
    except OSError as e:
        # Handle any OS-related errors and return a response
        return response.json({'error': str(e)}, status=500)

    # Return a success response
    return response.json({'message': 'Files renamed successfully'})

# Run the Sanic application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

"""
    This is a Sanic application serving as a batch file renaming tool.

    Features:
    - Renames files in a specified folder with a given prefix and suffix.
    - Handles errors such as invalid JSON payloads or OS-related errors.
    - Returns JSON responses indicating the success or failure of the operation.

    Usage:
    - POST to /rename/<folder_path> with JSON payload containing 'prefix' and 'suffix'.

    Example payload:
    {
        "prefix": "new_",
        "suffix": ".txt"
    }

    The folder path is expected to be encoded in the URL.

    Note:
    - Ensure the folder path is correct and accessible.
    - The tool assumes that the files to be renamed are directly in the specified folder.
    - Error handling is implemented to catch and respond to common issues.

    Author: Your Name
    Date: YYYY-MM-DD
"""
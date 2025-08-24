# 代码生成时间: 2025-08-25 03:21:08
import os
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import HTTPResponse

# Configuration manager application
app = Sanic("ConfigManager")

# Define the directory where configuration files are stored
CONFIG_DIR = "./configs"

# Check if the configuration directory exists, if not, create it
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# Error handler for configuration file not found
@app.exception(ServerError)
async def server_error(request: Request, exception: Exception):
    return response.json({"error": "Configuration file not found"}, status=404)

# Route to get a configuration file
@app.route("/config/<filename:path>", methods=["GET"])
async def get_config(request: Request, filename: str):
    # Check if the configuration file exists
    config_path = os.path.join(CONFIG_DIR, filename)
    if not os.path.isfile(config_path):
        raise ServerError
    # Read and return the configuration file content
    with open(config_path, "r") as config_file:
        config_content = config_file.read()
        return response.json(json.loads(config_content))

# Route to create or update a configuration file
@app.route("/config/<filename:path>", methods=["POST"])
async def set_config(request: Request, filename: str):
    try:
        # Get the configuration data from the request
        config_data = request.json
        # Write the configuration data to a file
        config_path = os.path.join(CONFIG_DIR, filename)
        with open(config_path, "w") as config_file:
            json.dump(config_data, config_file)
        return response.json(config_data)
    except json.JSONDecodeError:
        return response.json({"error": "Invalid JSON"}, status=400)

# Route to delete a configuration file
@app.route("/config/<filename:path>", methods=["DELETE"])
async def delete_config(request: Request, filename: str):
    # Check if the configuration file exists
    config_path = os.path.join(CONFIG_DIR, filename)
    if not os.path.isfile(config_path):
        raise ServerError
    # Remove the configuration file
    os.remove(config_path)
    return response.json({"message": "Configuration file deleted"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
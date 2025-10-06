# 代码生成时间: 2025-10-07 03:42:21
import hashlib
def calculate_file_hash(file_path):
    # Calculate the hash of a given file
    """
    This function calculates the SHA-256 hash of a file.

    Parameters:
        file_path (str): The path to the file for which the hash is to be calculated.

    Returns:
        str: The SHA-256 hash of the file content.
    """
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # Main function to check file integrity
    """
    This function sets up the Sanic web application and starts the file integrity checker.
    """
    from sanic import Sanic
    from sanic.response import json
    app = Sanic("FileIntegrityChecker")
    
    @app.route("/check", methods=["POST"])
    async def check_file(request):
        # Endpoint to check the file hash
        """
        This endpoint receives a file path and returns the SHA-256 hash.
        """
        file_path = request.json.get("file_path")
        if not file_path:
            return json({"error": "Missing file_path parameter"}, status=400)

        hash_result = calculate_file_hash(file_path)
        if hash_result is None:
            return json({"error": "Failed to calculate hash"}, status=500)
        return json({"file_path": file_path, "hash": hash_result})
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
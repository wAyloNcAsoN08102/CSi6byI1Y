# 代码生成时间: 2025-08-31 19:51:29
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.response import json
from sanic.exceptions import ServerError
import jsonpickle


# Initialize the application
app = Sanic("ThemeSwitcherService")


# Define a dictionary to hold user theme preferences
USER_THEME_PREFERENCES = {}


@app.route("/switch-theme", methods=["POST"])
async def switch_theme(request):
    """
    Switches the theme for a user based on the provided user ID and theme name.
    
    Args:
    - request: Sanic request object containing user ID and theme preference.
    
    Returns:
    - A JSON response indicating whether the theme was successfully switched.
    
    Raises:
    - ServerError if no user ID is provided or if the theme name is invalid.
    """
    try:
        # Extract user ID and theme from the request
        user_id = request.json.get("user_id")
        theme = request.json.get("theme")
        
        # Check if user ID and theme are provided
        if not user_id:
            raise ServerError("User ID is required", status_code=400)
        if not theme:
            raise ServerError("Theme name is required", status_code=400)
        
        # Update user theme preference
        USER_THEME_PREFERENCES[user_id] = theme
        
        # Return success response
        return response.json({"message": "Theme switched successfully"}, status=200)
    except Exception as e:
        # Handle any unexpected errors
        raise ServerError(str(e), status_code=500)


@app.route("/get-theme", methods=["GET"])
async def get_theme(request):
    """
    Retrieves the current theme for a user based on the provided user ID.
    
    Args:
    - request: Sanic request object containing user ID.
    
    Returns:
    - A JSON response containing the current theme for the user.
    
    Raises:
    - NotFound if no user ID is provided or if the theme preference is not found.
    """
    try:
        # Extract user ID from the request
        user_id = request.args.get("user_id")
        
        # Check if user ID is provided
        if not user_id:
            raise NotFound("User ID is required", status_code=400)
        
        # Retrieve user theme preference
        theme = USER_THEME_PREFERENCES.get(user_id)
        
        # Check if theme preference is found
        if not theme:
            raise NotFound("Theme preference not found", status_code=404)
        
        # Return the current theme for the user
        return response.json({"theme": theme}, status=200)
    except Exception as e:
        # Handle any unexpected errors
        raise ServerError(str(e), status_code=500)


if __name__ == "__main__":
    """
    Run the Sanic application.
    
    Usage:
    python theme_switcher_service.py
    """
    app.run(host="0.0.0.0", port=8000, debug=True)
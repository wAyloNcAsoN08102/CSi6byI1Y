# 代码生成时间: 2025-08-19 20:15:13
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.request import Request
from sanic.response import json

# Define the application
app = Sanic("MessageNotificationService")

# Mock database for storing user subscriptions
user_subscriptions = {}

# Define the route for sending notifications
@app.route("/notify", methods=["POST"])
async def notify(request: Request):
    # Get the notification message from the request
    notification = request.json
    if not notification:
        return response.json({"error": "No notification message provided"}, status=400)
    
    # Send notification to all subscribed users
    for user_id, subscriptions in user_subscriptions.items():
        for subscription in subscriptions:
            if notification["topic"] in subscription["topics"]:
                # Simulate sending a notification (in real case, use an email service or messaging system)
                print(f"Sending notification to {user_id} about {notification['topic']}")
    
    return response.json({"message": "Notification sent"})

# Define the route for user subscription
@app.route("/subscribe", methods=["POST"])
async def subscribe(request: Request):
    # Get the subscription data from the request
    subscription_data = request.json
    user_id = subscription_data.get("user_id")
    topics = subscription_data.get("topics")
    
    # Validate user_id and topics
    if not user_id or not topics:
        return response.json({"error": "Invalid subscription data"}, status=400)
    
    # Add or update the user's subscription
    if user_id not in user_subscriptions:
        user_subscriptions[user_id] = []
    user_subscriptions[user_id].append({"topics": topics})
    
    return response.json({"message": "Subscription updated"})

# Define the route for user unsubscription
@app.route("/unsubscribe", methods=["POST"])
async def unsubscribe(request: Request):
    # Get the unsubscription data from the request
    unsubscription_data = request.json
    user_id = unsubscription_data.get("user_id")
    topic = unsubscription_data.get("topic")
    
    # Validate user_id and topic
    if not user_id or not topic:
        return response.json({"error": "Invalid unsubscription data"}, status=400)
    
    # Remove the user's subscription
    if user_id in user_subscriptions:
        for subscription in user_subscriptions[user_id]:
            if topic in subscription["topics"]:
                subscription["topics"].remove(topic)
                if not subscription["topics"]:
                    user_subscriptions[user_id].remove(subscription)
                    break
                
        if not user_subscriptions[user_id]:
            del user_subscriptions[user_id]
    
    return response.json({"message": "Unsubscription successful"})

# Define the error handler for 404 errors
@app.exception(NotFound)
async def not_found_handler(request: Request, exception: NotFound):
    return response.json({"error": "Resource not found"}, status=404)

# Define the error handler for server errors
@app.exception(ServerError)
async def server_error_handler(request: Request, exception: ServerError):
    return response.json({"error": "Internal server error"}, status=500)

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
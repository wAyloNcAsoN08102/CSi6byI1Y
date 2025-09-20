# 代码生成时间: 2025-09-21 05:30:29
import asyncio
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json

# Define the SortingService class to encapsulate sorting logic
class SortingService:
    def __init__(self):
        pass

    # Bubble Sort algorithm implementation
    def bubble_sort(self, data):
        """Sorts the data list using the bubble sort algorithm.

        Args:
            data (list): The list of elements to sort.

        Returns:
            list: The sorted list."""
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

    # Insertion Sort algorithm implementation
    def insertion_sort(self, data):
        """Sorts the data list using the insertion sort algorithm.

        Args:
            data (list): The list of elements to sort.

        Returns:
            list: The sorted list."""
        for i in range(1, len(data)):
            key = data[i]
            j = i-1
            while j >= 0 and key < data[j]:
                data[j+1] = data[j]
                j -= 1
            data[j+1] = key
        return data

    # Selection Sort algorithm implementation
    def selection_sort(self, data):
        """Sorts the data list using the selection sort algorithm.

        Args:
            data (list): The list of elements to sort.

        Returns:
            list: The sorted list."""
        for i in range(len(data)):
            min_idx = i
            for j in range(i+1, len(data)):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
        return data

# Initialize the Sanic app
app = Sanic("SortingService")

# Instantiate the SortingService
sorting_service = SortingService()

# Define the route for sorting using bubble sort
@app.route("/bubble_sort", methods=["POST"])
async def bubble_sort(request: Request):
    # Extract data from the request body
    data = request.json.get("data")
    if not data:
        return response.json({"error": "No data provided"}, status=400)

    try:
        # Sort the data using bubble sort
        sorted_data = sorting_service.bubble_sort(data)
        return response.json({"sorted_data": sorted_data})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

# Define the route for sorting using insertion sort
@app.route("/insertion_sort", methods=["POST"])
async def insertion_sort(request: Request):
    # Extract data from the request body
    data = request.json.get("data")
    if not data:
        return response.json({"error": "No data provided"}, status=400)

    try:
        # Sort the data using insertion sort
        sorted_data = sorting_service.insertion_sort(data)
        return response.json({"sorted_data": sorted_data})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

# Define the route for sorting using selection sort
@app.route("/selection_sort", methods=["POST"])
async def selection_sort(request: Request):
    # Extract data from the request body
    data = request.json.get("data")
    if not data:
        return response.json({"error": "No data provided"}, status=400)

    try:
        # Sort the data using selection sort
        sorted_data = sorting_service.selection_sort(data)
        return response.json({"sorted_data": sorted_data})
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
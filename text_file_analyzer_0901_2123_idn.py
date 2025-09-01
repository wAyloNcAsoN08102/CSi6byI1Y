# 代码生成时间: 2025-09-01 21:23:04
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound, abort
import os

"""
Text File Analyzer Service
This service analyzes the content of a given text file.
It provides an endpoint to upload a text file and returns the file's unique words count.
"""

app = sanic.Sanic('TextFileAnalyzerService')

# Define a route for file upload and analysis
@app.route('/upload', methods=['POST'])
def analyze_text(request):
    # Check if the file is in the request
    file = request.files.get('file')
    if not file:
        abort(400, 'No file provided')
    
    try:
        # Save the file to a temporary location
        file_path = save_file(file)
        # Analyze the file content and get unique words count
        unique_words_count = analyze_file(file_path)
        # Return the result
        return json({'file_name': file.filename, 'unique_words_count': unique_words_count})
    except Exception as e:
        raise ServerError('An error occurred while processing the file', e)

# Function to save the uploaded file
def save_file(file):
    """
    Save the uploaded file to a temporary location.
    :return: path to the saved file
    """
    file_path = os.path.join('temp', file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.body)
    return file_path

# Function to analyze the file content
def analyze_file(file_path):
    """
    Analyze the file content and return the number of unique words.
    :param file_path: path to the file
    :return: number of unique words
    """
    unique_words = set()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                words = line.split()
                unique_words.update(words)
        return len(unique_words)
    except FileNotFoundError:
        abort(404, 'File not found')
    except Exception as e:
        raise ServerError('Failed to analyze the file', e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
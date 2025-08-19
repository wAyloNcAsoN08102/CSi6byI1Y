# 代码生成时间: 2025-08-19 13:45:40
import asyncio
from sanic import Sanic
from sanic.response import json
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.oxml import parse_xml
from docx.oxml.ns import qn
import mimetypes
import os
import base64
import tempfile
import datetime

# Initialize the Sanic application
app = Sanic('document_converter')

# Define the routes for the document converter
@app.route('/upload', methods=['POST'])
def upload_file(request):
    """Handle file uploads."""
    file = request.files.get('file')
    if not file:
        return json({'error': 'No file provided'}, status=400)

    file_path = os.path.join(tempfile.gettempdir(), file.name)
    with open(file_path, 'wb') as f:
        f.write(file.body)

    try:
        convert_to_pdf(file_path)
        return json({'message': 'File converted successfully'}, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)

@app.route('/convert', methods=['POST'])
def convert_document(request):
    """Convert the uploaded document to PDF."""
    file_path = request.json.get('file_path')
    if not file_path:
        return json({'error': 'No file path provided'}, status=400)

    try:
        convert_to_pdf(file_path)
        return json({'message': 'File converted successfully'}, status=200)
    except Exception as e:
        return json({'error': str(e)}, status=500)

def convert_to_pdf(file_path):
    """Convert a document to PDF."""
    # Check the file extension
    _, file_ext = os.path.splitext(file_path)

    # Convert DOCX to PDF
    if file_ext.lower() == '.docx':
        doc = Document(file_path)
        for para in doc.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.save(os.path.splitext(file_path)[0] + '.pdf')
    else:
        raise ValueError('Unsupported file format')

# Run the Sanic application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

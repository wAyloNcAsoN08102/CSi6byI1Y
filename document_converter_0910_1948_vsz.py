# 代码生成时间: 2025-09-10 19:48:33
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerNotReady
from sanic.request import Request
from sanic.response import HTTPResponse
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Define the Sanic app
app = Sanic('Document Converter')

# Home route to display welcome message
@app.route('/')
async def index(request: Request):
    return response.json({'message': 'Welcome to the Document Converter!'})

# Route to convert Word document to PDF
@app.route('/convert/to_pdf', methods=['POST'])
async def convert_to_pdf(request: Request):
    try:
        # Get the uploaded file from the request
        file = request.files.get('file')
        if not file:
            return response.json({'error': 'No file uploaded'}, status=400)

        # Save the file to a temporary location
        with open('temp.docx', 'wb') as f:
            f.write(file.body)

        # Load the Word document
        doc = Document('temp.docx')

        # Add a new paragraph with a welcome message
        doc.add_paragraph('Hello, welcome to the Document Converter!')

        # Save the document as a PDF
        doc.save('temp.pdf')

        # Return the file contents as a response
        return response.file('temp.pdf')
    except Exception as e:
        # Handle any exceptions that occur during the conversion process
        return response.json({'error': str(e)}, status=500)
    finally:
        # Clean up any temporary files
        if os.path.exists('temp.docx'):
            os.remove('temp.docx')
        if os.path.exists('temp.pdf'):
            os.remove('temp.pdf')

# Run the app
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, workers=2)
    except ServerNotReady as e:
        raise ServerError(e)
    except Exception as e:
        raise ServerError(e)
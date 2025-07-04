from flask import Flask, request, jsonify, Response
import pytesseract
from PIL import Image
import zipfile
import io
import json
from pdf2image import convert_from_bytes
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to OCR server.'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    pdf_file = request.files['file']
    images = convert_from_bytes(pdf_file.read())

    results = {}
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang='jpn')
        results['page-' + str(i+1)] = text

    return Response(json.dumps(results, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

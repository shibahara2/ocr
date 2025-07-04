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
    
    uploaded_file = request.files['file']
    filename = uploaded_file.filename.lower()

    if filename.endswith('.pdf'):
        images = convert_from_bytes(uploaded_file.read())
    elif filename.endswith('.png') or filename.endswith('.jpg'):
        image = Image.open(uploaded_file.stream)
        images = [image]
    else:
        return jsonify({'error': 'Unsupported file type'}), 415

    results = {}
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang='jpn')
        results['page-' + str(i+1)] = text

    return Response(json.dumps(results, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

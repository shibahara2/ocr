from flask import Flask, request, jsonify, Response
import pytesseract
from PIL import Image
import zipfile
import io
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to OCR server.'

@app.route('/ocr', methods=['POST'])
def ocr_zip():
    if 'zip' not in request.files:
        return jsonify({'error': 'No zip file uploaded'}), 400

    zip_file = request.files['zip']
    zip_bytes = io.BytesIO(zip_file.read())  # ← ここで BytesIO に変換
    results = {}

    with zipfile.ZipFile(zip_bytes) as z:
        for filename in z.namelist():
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                with z.open(filename) as image_file:
                    image = Image.open(image_file)
                    text = pytesseract.image_to_string(image, lang='jpn')
                    results[filename] = text

    return Response(json.dumps(results, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

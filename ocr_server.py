from flask import Flask, request, jsonify, Response
import pytesseract
from PIL import Image
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to OCR server.'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    text = pytesseract.image_to_string(image)
    return Response(json.dumps({'text': text}, ensure_ascii=False))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

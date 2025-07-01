from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    text = pytesseract.image_to_string(image)
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

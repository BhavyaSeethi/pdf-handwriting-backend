from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "PDF Handwriting Backend is running"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    handwriting = request.files.get('handwriting')

    if not file or not handwriting:
        return "Missing file or handwriting image", 400

    # Simulate conversion: create a blank image with sample text
    img = Image.new('RGB', (800, 1000), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 100), f"Converted: {file.filename}", fill='black')

    buf = io.BytesIO()
    img.save(buf, format='PDF')
    buf.seek(0)

    return send_file(buf, as_attachment=True, download_name='handwritten.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

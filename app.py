from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import cv2
import os
import io

app = Flask(__name__)

# Step 1: Extract handwritten characters from image
def extract_handwritten_chars(image_path, output_folder='handwritten_chars'):
    os.makedirs(output_folder, exist_ok=True)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    char_map = {}
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        char_img = img[y:y+h, x:x+w]
        resized = cv2.resize(char_img, (40, 40))
        filename = f'{output_folder}/char_{i}.png'
        cv2.imwrite(filename, resized)
        char_map[f'char_{i}'] = filename
    return char_map

@app.route('/')
def home():
    return "✅ PDF Handwriting Backend is running"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('pdf') or request.files.get('file')
    handwriting = request.files.get('handwriting')

    if not file or not handwriting:
        return "❌ Missing file or handwriting image", 400

    # Save uploaded files
    os.makedirs('uploads', exist_ok=True)
    pdf_path = os.path.join('uploads', file.filename)
    handwriting_path = os.path.join('uploads', handwriting.filename)
    file.save(pdf_path)
    handwriting.save(handwriting_path)

    # Step 1: Extract characters
    char_map = extract_handwritten_chars(handwriting_path)

    # Simulated preview output
    img = Image.new('RGB', (800, 1000), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 100), f"✅ Extracted {len(char_map)} characters from handwriting", fill='black')
    draw.text((50, 160), f"📄 Uploaded file: {file.filename}", fill='black')
    draw.text((50, 220), f"🖋️ Handwriting image: {handwriting.filename}", fill='black')

    buf = io.BytesIO()
    img.save(buf, format='PDF')
    buf.seek(0)

    return send_file(buf, as_attachment=True, download_name='handwritten_preview.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from detect import detect
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import cv2

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = './uploads'

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_image():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(415)
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(file_path)
        
        # Call the detect function and get the result
        result = detect(file_path)
        
        return jsonify({'file_url': url_for('upload', filename=filename, _external=True), 'label': result['label'], 'percent': result['probability']})
    return jsonify({'error': 'No file uploaded'}), 400

@app.route('/detect_person', methods=['POST'])
@cross_origin()
def detect_person():
    data = request.json
    startX = data.get('startX')
    startY = data.get('startY')
    endX = data.get('endX')
    endY = data.get('endY')
    img_path = data.get('file_url')

    # Load the image
    image = cv2.imread(img_path)
    cropped_image = image[startY:endY, startX:endX]

    # Save the cropped image temporarily
    temp_path = os.path.join(app.config['UPLOAD_PATH'], 'temp.jpg')
    cv2.imwrite(temp_path, cropped_image)

    # Call the detect function and get the result
    result = detect(temp_path)

    return jsonify({'label': result['label'], 'percent': result['probability']})

@app.route('/download_report', methods=['POST'])
@cross_origin()
def download_report():
    data = request.json
    label = data.get('label')
    probability = data.get('percent')
    imgpath = data.get('file_url')

    # Create PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, f"Kết quả phân tích ảnh")
    c.drawString(100, height - 120, f"Đường dẫn ảnh: {imgpath}")
    c.drawString(100, height - 140, f"Nhãn: {label}")
    c.drawString(100, height - 160, f"Độ tin cậy: {probability}%")

    # Add image to PDF
    if os.path.exists(imgpath):
        c.drawImage(imgpath, 100, height - 300, width=200, height=200)

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'message': 'Kích thước file quá lớn, vui lòng upload file < 5MB'}), 413

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({'message': 'Định dạng file không được hỗ trợ, vui lòng upload file jpg/png/jpeg'}), 415

@app.route('/uploads/<filename>')
@cross_origin()
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/assets/<path:path>')
@cross_origin()
def asset(path):
    return send_from_directory('assets', path)

if __name__ == "__main__":
    app.run(debug=True)
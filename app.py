import imghdr
import os
from flask import Flask,send_file, render_template, request, flash, redirect, url_for, abort, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from detect import detect
import uuid
import io
from reportlab.lib.pagesizes import letter  # Import letter
from reportlab.pdfgen import canvas  # Import canvas

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = './uploads'

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/download_report', methods=['POST'])
@cross_origin()
def download_report():
    data = request.json
    label = data.get('label')
    probability = data.get('percent')
    imgpath = data.get('file_url')

    # Tạo PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 50, "DEEPFAKE DETECTION REPORT")

    # Add content
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 140, f"Image URL: {imgpath}")
    c.drawString(100, height - 170, f"Result: {label}")
    c.drawString(100, height - 200, f"Probability: {probability}%")


    # Add timestamp
    from datetime import datetime
    gmt_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S GMT')
    c.drawString(100, height - 230, f"Timestamp: {gmt_time}")

    # Thêm ảnh vào PDF
    if os.path.exists(imgpath):
        c.drawImage(imgpath, 100, height - 300, width=200, height=200)

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')
    # upload original img
@app.route('/', methods=['POST'])
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
        
        return jsonify({'file_url': url_for('upload', filename=filename, _external=True), 'label': result['label'], 'percent':result['probability']})
    return jsonify({'error': 'No file uploaded'}), 400

# upload cropped img
@app.route('/upload_with_box', methods=['POST'])
@cross_origin()
def upload_with_box():
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
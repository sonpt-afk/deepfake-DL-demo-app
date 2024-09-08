import imghdr
import os
from flask import Flask, render_template, request, flash, redirect, url_for, abort, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from detect import detect
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = './uploads'
app.secret_key = 'supersecretkey'

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
@cross_origin()
@app.route('/', methods=['POST'])
@cross_origin()
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            abort(400)
        file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(file_path)
        
        # Call the detect function and get the result
        result = detect(file_path, filename)
        
        return jsonify({'file_url': url_for('upload', filename=filename, _external=True), 'label': result['label']})
    return jsonify({'error': 'No file uploaded'}), 400
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

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
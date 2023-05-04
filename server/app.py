from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from pydub import AudioSegment
import subprocess

app = Flask(__name__, static_folder='../client/public', static_url_path='/')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024  # Max 24 MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    return app.send_static_file('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_audio(input_path, output_path):
    subprocess.call(['C:/ffmpeg/bin/ffmpeg.exe', '-i',
                    input_path, '-y', output_path])


@app.route('/convert', methods=['POST'])
def home():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Filetype not allowed'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Convert file to wav
    try:
        convert_audio(filepath, os.path.join(
            app.config['UPLOAD_FOLDER'], os.path.splitext(filename)[0] + '.wav'))
    except Exception as e:
        os.remove(filepath)
        return jsonify({'error': str(e)}), 400

    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.splitext(filename)[0] + '.wav', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

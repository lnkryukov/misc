from flask import Flask, request, render_template, send_from_directory
import uuid
import os
import logging
import hashlib

import fileManager

logging.getLogger().setLevel(0)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/avatar', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file found", 403
    file = request.files['file']
    if file.filename == '':
        return 'No file found', 403
    logging.info('Recieved file with content-length set as {}'.format(file.content_length))
    try:
        fileManager.saveAvatar(file, 'avatar')
    except fileManager.FileSizeLimitError as e:
        return e.message, 413
    except (fileManager.FileExtensionError, fileManager.FileMimeTypeError) as e:
        return e.message, 415
    return 'Saved', 200

@app.route('/avatar/<path:filename>')
def getAvatar(filename):
    return send_from_directory(fileManager.FILE_UPLOADS['FILE_SETS']['AVATAR']['FOLDER'], filename, as_attachment=False)
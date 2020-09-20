from flask import Flask
from os import getenv
import os

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

import routes
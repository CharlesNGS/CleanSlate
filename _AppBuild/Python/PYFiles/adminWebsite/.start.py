import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, session, redirect, url_for, send_from_directory, jsonify, request
from signin import checkPassword
from ..adminFunctions import multipleNewProduct

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'secretKey'

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return 'homepage'

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype.html')

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if not session.get('authenticated'):
        return redirect(url_for('page1'))
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype2.html')

@app.route('/authentication', methods=['POST'])
def authentication():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username)
    print(password)
    CheckPassword = checkPassword(username, password)

    if CheckPassword:
        session['authenticated'] = True
        return jsonify({'status': 'success', 'redirect': '/page2'}), 200
    else:
        return jsonify({'status': 'unauthorized'}), 401

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if not session.get('authenticated'):
        return redirect(url_for('page1'))
    
    if 'file' not in request.files:
        return {'status': 'error', 'message': 'No file part in the request'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'status': 'error', 'message': 'No selected file'}, 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = secure_filename(file.filename)
    unique_filename = f"{timestamp}_{filename}"

    save_path = os.path.join(r"D:\CleanSlate\_AppBuild\Python\Referenced Files", unique_filename)
    file.save(save_path)

    multipleNewProduct(save_path)

    os.remove(save_path)

    return {'status': 'success', 'saved_as': unique_filename}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

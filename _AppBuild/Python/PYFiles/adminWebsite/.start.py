import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, session, redirect, url_for, send_from_directory, jsonify, request
from signin import checkPassword
from PYFiles.adminFunctions.NewProduct import multipleNewProduct
from PYFiles.adminFunctions.NewCompany import addCompanyToCompanyDatabase

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'secretKey'

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return 'homepage'

#sign in
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype.html')

#Select function
@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if not session.get('authenticated'):
        return redirect(url_for('page1'))
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype1.html')

#Create new product
@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if not session.get('authenticated'):
        return redirect(url_for('page1'))
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype2.html')

#Create new company
@app.route('/page4', methods=['GET', 'POST'])
def page4():
    if not session.get('authenticated'):
        return redirect(url_for('page1'))
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype3.html')

#Update existing product
@app.route('/page5', methods=['GET', 'POST'])
def page5():
    if not session.get('authenticated'):
        return redirect(url_for('page1'))
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype4.html')

#Update existing company
@app.route('/page6', methods=['GET', 'POST'])
def page6():
    if not session.get('authenticated'):
        return redirect(url_for('page1'))
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype5.html')



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

    save_path = str(os.path.join(r"D:\CleanSlate\_AppBuild\Python\Referenced Files", unique_filename))
    print(save_path)
    file.save(save_path)

    multipleNewProduct(save_path)

    os.remove(save_path)

    return {'status': 'success', 'saved_as': unique_filename}, 200

@app.route('/addCompany', methods=['POST'])
def addCompany():
    data = request.get_json()
    companyName = data.get('company')
    AddCompany = addCompanyToCompanyDatabase(companyName)
    
    if AddCompany:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'unauthorized'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

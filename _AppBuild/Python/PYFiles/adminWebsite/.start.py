from flask import Flask, send_from_directory, jsonify, request
from signin import checkPassword

app = Flask(__name__, instance_relative_config=True)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return 'homepage'

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype.html')

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    return send_from_directory(r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype2.html')

@app.route('/authentication', methods=['POST'])
def authentication():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    CheckPassword = checkPassword(username, password)

    if CheckPassword:
        return jsonify({'status': 'success', 'redirect': r'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React\prototype2.html'}), 200
    else:
        return jsonify({'status': 'unauthorized'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

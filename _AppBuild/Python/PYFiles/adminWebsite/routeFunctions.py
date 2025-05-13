from flask import jsonify, request
from hashlib import sha256
from DataBaseConnections import accountDatabase
from PYFiles import app
from signin import checkPassword

@app.route('/authentication', methods=['POST'])
def authentication():    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    CheckPassword = checkPassword(username, password)
    
    if CheckPassword:
        return jsonify({'status': 'success', 'redirect': 'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React\prototype2.html'}), 200
    else:
        return jsonify({'status': 'unauthorized'}), 401
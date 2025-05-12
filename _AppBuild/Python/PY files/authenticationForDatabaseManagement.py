from flask import Flask, send_from_directory, jsonify, request
from hashlib import sha256
from DataBaseConnections import accountDatabase

app = Flask(__name__)

@app.route('/authentication', methods=['POST'])
def authentication():    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username)
    print(password)
    password = sha256(password.encode('utf-8')).hexdigest()

    AccountDataBase = accountDatabase()
    CheckPasswordQuery = "SELECT password FROM users WHERE username = %s"

    PasswordCheckInuseraccountDataBase = AccountDataBase.cursor()
    PasswordCheckInuseraccountDataBase.execute(CheckPasswordQuery, (username,))
    PasswordCheckInuseraccountDataBaseResult = PasswordCheckInuseraccountDataBase.fetchone()
    if PasswordCheckInuseraccountDataBaseResult:
    
        databasePassword = PasswordCheckInuseraccountDataBaseResult[0]

        if databasePassword == password:
            print("Auth True")
            return jsonify({'status': 'success', 'redirect': 'D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React\prototype2.html'}), 200
        else:
            print("Auth False for databasePassword")
            return jsonify({'status': 'unauthorized'}), 401
    else:
        print("Auth False for PasswordCheckInuseraccountDataBaseResult")
        return jsonify({'status': 'unauthorized'}), 401
    
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    return send_from_directory('D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype.html')

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    return send_from_directory('D:\CleanSlate\_AppBuild\Javascript\HTML with embeded React', 'prototype2.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

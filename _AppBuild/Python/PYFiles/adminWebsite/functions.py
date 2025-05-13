from flask import jsonify, request
from hashlib import sha256
from DataBaseConnections import accountDatabase
from PYFiles import app

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
from flask import Flask, request, jsonify
from hashlib import sha256
from DataBaseConnections import accountDatabase


app = Flask(__name__)

@app.route('/authentication', methods=['POST'])
def authentication():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
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
            return jsonify({'status': 'success'}), 200
        else:
            print("Auth False")
            return jsonify({'status': 'unauthorized'}), 401
    else:
        print("Auth False")
        return jsonify({'status': 'unauthorized'}), 401

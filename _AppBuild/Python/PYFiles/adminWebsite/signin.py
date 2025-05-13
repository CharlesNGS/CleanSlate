#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
sys.path.append(r'D:\CleanSlate\_AppBuild\Python')
from hashlib import sha256
from PYFiles.DataBaseConnections import accountDatabase


def checkPassword(username, password):
    password = sha256(password.encode('utf-8')).hexdigest()
    #Database connection specifying the host address, port, user, password from ENV file and the schema to use for quering the database.
    AccountDataBase = accountDatabase()
    CheckQuery = "SELECT passwordHash FROM accounts WHERE username = %s"
    
    PasswordDatabaseCheck = AccountDataBase.cursor()
    PasswordDatabaseCheck.execute(CheckQuery, (username,))
    PasswordDatabaseCheckResult = PasswordDatabaseCheck.fetchone()

    if PasswordDatabaseCheckResult:
        databasePassword = PasswordDatabaseCheckResult[0]
        if databasePassword == password:
            return True
        else:
            return False
    else:
        return False

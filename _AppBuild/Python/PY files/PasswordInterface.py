#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from dotenv import load_dotenv
from hashlib import sha256
import mysql.connector

def inputHash(password):
    preHashDetails = (password).encode('utf-8')
    PasswordHash = sha256(preHashDetails).hexdigest()
    return PasswordHash


def checkPassword(username):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\QRPasswordenv.env")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    PasswordDataBase = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="password_db"
    )

    CheckQuery = "SELECT passwordHash FROM accounts WHERE username = %s"
    PasswordDatabaseCheck = PasswordDataBase.cursor()
    PasswordDatabaseCheck.execute(CheckQuery, (username,))
    PasswordDatabaseCheckResult = PasswordDatabaseCheck.fetchone()
    PasswordDatabaseCheck.close()
    PasswordDataBase.close()
    return PasswordDatabaseCheckResult

def passwordCompare(PasswordHash, PasswordDatabaseCheckResult):
    if PasswordHash == PasswordDatabaseCheckResult:
        print("Access Allowed")
        return True
    else:
        print("Access Denied")
        return False

def completePasswordCheck(username, password):
    PasswordHash = inputHash(password)
    PasswordDatabaseCheckResult = checkPassword(username)
    AllowDeny = passwordCompare(PasswordHash, PasswordDatabaseCheckResult)
    return AllowDeny
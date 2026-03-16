#Imported modules
import sys
from pathlib import Path
rootDirectory = Path(__file__).resolve()
while not (rootDirectory / "_AppBuild").exists():
    rootDirectory = rootDirectory.parent
sys.path.append(rootDirectory)
from hashlib import sha256
from DataBaseConnections import accountDatabase


def checkPassword(username, password):
    password = sha256(password.encode('utf-8')).hexdigest()
    #Database connection specifying the host address, port, user, password from ENV file and the schema to use for quering the database.
    AccountDataBase = accountDatabase()
    CheckQuery = "SELECT password FROM users WHERE username = %s"
    print(username)
    print(password)
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

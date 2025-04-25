#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from dotenv import load_dotenv
import mysql.connector
import os
import re

#Function for testing if the input is valid. This helps prevent SQL injection and wasted processing.
def hashValidation(QRHashInput):
    # SHA256 hash is 64 characters and only uses characters a-f, A-F and 0-9
    if len(QRHashInput) == 64 and re.fullmatch(r'^[0-9a-fA-F]{64}$', QRHashInput):
        print("This is a hash")
        return True
    else:
        print("no hash")
        return False

#Estabilishes a connection to the database. Sends the query to the database with the verified hash. Returns the result associated with the hash if one exists.
def hashCheck(QRHashInput):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path="D:\CleanSlate\_AppBuild\Python\Imports\QRPasswordenv.env")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    QRDataBase = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )
    
    #Stores the query itself and allows the hash input to be a variable.
    Query = "SELECT translation FROM qrtable WHERE qrHash = %s"
    QRDatabaseQuery = QRDataBase.cursor()
    QRDatabaseQuery.execute(Query, (QRHashInput,))
    QRDatabaseResult = QRDatabaseQuery.fetchone()

    #If there is a result it returns the information corresponding to the result.
    if QRDatabaseResult:
        print(f"{QRHashInput} Exists and the associated information is: {QRDatabaseResult[0]}")
        QRDatabaseQuery.close()
        QRDataBase.close()
    #If there is no result it confirms that there is no result.
    else:
        print(f"There is no sign of {QRHashInput} in the database.")
        QRDatabaseQuery.close()
        QRDataBase.close()

#Merges both functions into one function to be imported by the listening file. Adding a quit function for invalid inputs.
def completeQuery(QRHashInput): 
    if hashValidation(QRHashInput) is False:
        print("Is false")
        quit()
    else:
        print("Is True")
        hashCheck(QRHashInput)
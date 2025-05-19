#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
#import mysql.connector
from PYFiles.DataBaseConnections import productDatabase
import re

#Function for testing if the input is valid. This helps prevent SQL injection and wasted processing.
def hashValidation(HashInput):
    # SHA256 hash is 64 characters and only uses characters a-f, A-F and 0-9
    if len(HashInput) == 64 and re.fullmatch(r'^[0-9a-fA-F]{64}$', HashInput):
        return True
    else:
        return False

#Estabilishes a connection to the database. Sends the query to the database with the verified hash. Returns the result associated with the hash if one exists.
def hashCheck(HashInput):

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    QRDataBase = productDatabase

    #Stores the query itself and allows the hash input to be a variable.
    HashCheckInProductDatabaseQuery = "SELECT translation FROM qrtable WHERE qrHash = %s"

    HashCheckInProductDatabase = QRDataBase.cursor()
    HashCheckInProductDatabase.execute(HashCheckInProductDatabaseQuery, (HashInput,))
    HashCheckInProductDatabaseResult = HashCheckInProductDatabase.fetchone()

    #If there is a result it returns the information corresponding to the result.
    if HashCheckInProductDatabaseResult:
        print(f"{HashInput} Exists and the associated information is: {HashCheckInProductDatabaseResult[0]}")
        HashCheckInProductDatabase.close()
        QRDataBase.close()
    #If there is no result it confirms that there is no result.
    else:
        print(f"There is no sign of {HashInput} in the database.")
        HashCheckInProductDatabase.close()
        QRDataBase.close()

#Merges both functions into one function to be imported by the listening file. Adding a quit function for invalid inputs.
def completeQuery(HashInput): 
    if hashValidation(HashInput) is False:
        print("The received product information has been sent in a malformed formate. This is the result of attempted Database tampering. LOL")
        quit()
    else:
        print("Reteiving product details now")
        hashCheck(HashInput)
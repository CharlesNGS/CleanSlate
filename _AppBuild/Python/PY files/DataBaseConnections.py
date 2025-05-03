#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from dotenv import load_dotenv
import mysql.connector
import os

def companyDatabase():
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\QRPasswordenv.env")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    CompanyDataBase = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )
    return CompanyDataBase

def productDatabase():
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\Python")

    ProductDataBase = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )
    return ProductDataBase
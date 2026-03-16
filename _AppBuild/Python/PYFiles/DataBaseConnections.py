#Imported modules
import sys
from pathlib import Path
rootDirectory = Path(__file__).resolve()
while not (rootDirectory / "_AppBuild").exists():
    rootDirectory = rootDirectory.parent
sys.path.append(rootDirectory)
from dotenv import load_dotenv
import mysql.connector
import os

def companyDatabase():
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=rootDirectory / "_AppBuild/Python/Referenced Files/DatabaseENV.env")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    CompanyDataBase = mysql.connector.connect(
        host=os.getenv("MYSQLIP"),
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )
    return CompanyDataBase

def productDatabase():
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=rootDirectory / "_AppBuild/Python/Referenced Files/DatabaseENV.env")

    ProductDataBase = mysql.connector.connect(
        host=os.getenv("MYSQLIP")
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )
    return ProductDataBase

def accountDatabase():
    
    load_dotenv(dotenv_path=rootDirectory / "_AppBuild/Python/Referenced Files/DatabaseENV.env")
    
    ProductDataBase = mysql.connector.connect(
        host=os.getenv("MYSQLIP")
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="useraccount"
    )
    return accountDatabase
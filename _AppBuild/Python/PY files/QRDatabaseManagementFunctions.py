#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from DataBaseConnections import companyDatabase
from DataBaseConnections import productDatabase
from dotenv import load_dotenv

def addProductToDatabase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    ProductDataBase = productDatabase
    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    CompanyDataBase = companyDatabase

    #Stores the query to check if the hash is in the database.
    CheckCompanyQuery = "SELECT * FROM allowedcompanies WHERE allowedcompanieslist = %s"
    #Stores the query to check if the hash is in the database.
    CheckProductQuery = "SELECT * FROM qrtable WHERE qrhash = %s"
    #Stores the query to add the new data to the database.
    InsertProductQuery = "INSERT INTO qrtable (qrhash, translation, Company, SKU) Values (%s, %s, %s, %s)"

    #Check to see if an object already exists in the database
    CompanyDatabaseCheck = CompanyDataBase.cursor()
    CompanyDatabaseCheck.execute(CheckCompanyQuery, (ProductTuple[PositionOfCompanyName],))
    CompanyDatabaseCheckResult = CompanyDatabaseCheck.fetchone()

    #Check to see if an object already exists in the database
    ProductDatabaseCheck = ProductDataBase.cursor()
    ProductDatabaseCheck.execute(CheckProductQuery, (QRHash,))
    ProductDatabaseCheckResult = ProductDatabaseCheck.fetchone()

    #If the QR code already exists
    if not CompanyDatabaseCheckResult:
        print(f"The company {ProductTuple[PositionOfCompanyName]} has not yet been setup.")
        CompanyDatabaseCheck.close()
        CompanyDataBase.close()
    #If the QR code already exists
    elif ProductDatabaseCheckResult:
        print("This product has already been added to the database.")
        ProductDatabaseCheck.close()
        ProductDataBase.close()
        return False
    else:
        ProductDatabaseAdd = ProductDataBase.cursor()
        ProductDatabaseAdd.execute(InsertProductQuery, (QRHash, ProductTuple[PositionOfTranslation], ProductTuple[PositionOfCompanyName], ProductTuple[PositionOfProductSKU]))
        ProductDataBase.commit()
        ProductDatabaseAdd.close()
        ProductDataBase.close()
        return True

def addCompanyToDatabase(newCompanyName):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\QRPasswordenv.env")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    CompanyDataBase = companyDatabase()

    #Stores the query to check if the company exists in the database.
    CheckQuery = "SELECT allowedcompanieslist FROM allowedcompanies WHERE allowedcompanieslist = %s"
    #Stores the query to add the new data to the database.
    InsertQuery = "INSERT INTO allowedcompanies (allowedcompanieslist) Values (%s)"

    #Check to see if an object already exists in the database
    CompanyDatabaseCheck = CompanyDataBase.cursor()
    CompanyDatabaseCheck.execute(CheckQuery, (newCompanyName,))
    CompanyDatabaseCheckResult = CompanyDatabaseCheck.fetchone()
    #If the QR code already exists
    if CompanyDatabaseCheckResult:
        print("This company has already been added to the database.")
        CompanyDatabaseCheck.close()
        CompanyDataBase.close()
    else:
        CompanyDatabaseAdd = CompanyDataBase.cursor()
        CompanyDatabaseAdd.execute(InsertQuery, (newCompanyName,))
        CompanyDataBase.commit()
        CompanyDatabaseAdd.close()
        CompanyDataBase.close()
        print("This company has now been added to the database.")

def updateTranslationInDatabase(ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\Python")

    ProductDataBase = productDatabase()

    #Stores the query to check if the company exists is in the database.
    CheckProductSKUQuery = "SELECT SKU FROM qrtable WHERE SKU = %s"
    #Stores the query to add the new data to the database.
    CheckCompanyNameQuery = "SELECT Company FROM qrtable WHERE Company = %s"

    UpdateQuery = "UPDATE qrtable SET translation = %s WHERE SKU = %s and Company = %s"

    #Check to see if an object already exists in the database
    ProductSKUCheck = ProductDataBase.cursor()
    ProductSKUCheck.execute(CheckProductSKUQuery, (ProductTuple[PositionOfProductSKU],))
    ProductSKUCheckResult = ProductSKUCheck.fetchone()

    #Check to see if an object already exists in the database
    CompanyCheck = ProductDataBase.cursor()
    CompanyCheck.execute(CheckCompanyNameQuery, (ProductTuple[PositionOfCompanyName],))
    CompanyCheckResult = CheckCompanyNameQuery.fetchone()

    if ProductSKUCheckResult and CompanyCheckResult:
        TranslationUpdate = ProductDataBase.cursor()
        TranslationUpdate.execute(UpdateQuery, (ProductTuple[PositionOfTranslation], ProductTuple[PositionOfProductSKU], ProductTuple[PositionOfCompanyName],))
        TranslationUpdate.commit()
        ProductDataBase.close()
        ProductDataBase.close()
    else:
        print("Unable to update database existing entry does not exist.")
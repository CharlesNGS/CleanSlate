#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from _AppBuild.Python.Imports.DataBaseConnections import companyDatabase
from _AppBuild.Python.Imports.DataBaseConnections import productDatabase
from dotenv import load_dotenv

def addProductToProductDatabase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    ProductDataBase = productDatabase
    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    CompanyDataBase = companyDatabase

    #Stores the query to check if the hash is in the database.
    CompanyCheckInCompanyDataBaseQuery = "SELECT allowedcompanieslist FROM allowedcompanies WHERE allowedcompanieslist = %s"
    #Stores the query to check if the hash is in the database.
    HashCheckInProductDataBaseQuery = "SELECT * FROM qrtable WHERE qrhash = %s"
    #Stores the query to add the new data to the database.
    ProductInsertProductDataBaseQuery = "INSERT INTO qrtable (qrhash, translation, Company, SKU) Values (%s, %s, %s, %s)"

    #Check to see if an object already exists in the database
    CompanyCheckInCompanyDataBase = CompanyDataBase.cursor()
    CompanyCheckInCompanyDataBase.execute(CompanyCheckInCompanyDataBaseQuery, (ProductTuple[PositionOfCompanyName],))
    CompanyCheckInCompanyDataBaseResult = CompanyCheckInCompanyDataBase.fetchone()

    #Check to see if an object already exists in the database
    ProductCheckInProductDatabase = ProductDataBase.cursor()
    ProductCheckInProductDatabase.execute(HashCheckInProductDataBaseQuery, (QRHash,))
    ProductCheckInProductDatabaseResult = ProductCheckInProductDatabase.fetchone()

    #If the QR code already exists
    if not CompanyCheckInCompanyDataBaseResult:
        print(f"The company {ProductTuple[PositionOfCompanyName]} has not yet been setup.")
        CompanyCheckInCompanyDataBaseResult.close()
        CompanyDataBase.close()
    #If the QR code already exists
    elif ProductCheckInProductDatabaseResult:
        print("This product has already been added to the database.")
        ProductCheckInProductDatabase.close()
        ProductDataBase.close()
        return False
    else:
        ProductDatabaseAdd = ProductDataBase.cursor()
        ProductDatabaseAdd.execute(ProductInsertProductDataBaseQuery, (QRHash, ProductTuple[PositionOfTranslation], ProductTuple[PositionOfCompanyName], ProductTuple[PositionOfProductSKU]))
        ProductDataBase.commit()
        ProductDatabaseAdd.close()
        ProductDataBase.close()
        return True

def addCompanyToCompanyDatabase(newCompanyName):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\QRPasswordenv.env")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    CompanyDataBase = companyDatabase()

    #Stores the query to check if the company exists in the database.
    CompanyCheckInCompanyDataBaseQuery = "SELECT allowedcompanieslist FROM allowedcompanies WHERE allowedcompanieslist = %s"
    #Stores the query to add the new data to the database.
    CompanyInsertInCompanyDataBaseQuery = "INSERT INTO allowedcompanies (allowedcompanieslist) Values (%s)"

    #Check to see if an object already exists in the database
    CompanyCheckInCompanyDataBase = CompanyDataBase.cursor()
    CompanyCheckInCompanyDataBase.execute(CompanyCheckInCompanyDataBaseQuery, (newCompanyName,))
    CompanyCheckInCompanyDataBaseResult = CompanyCheckInCompanyDataBase.fetchone()
    #If the QR code already exists
    if CompanyCheckInCompanyDataBaseResult:
        print("This company has already been added to the database.")
        CompanyCheckInCompanyDataBase.close()
        CompanyDataBase.close()
    else:
        CompanyDatabaseAdd = CompanyDataBase.cursor()
        CompanyDatabaseAdd.execute(CompanyInsertInCompanyDataBaseQuery, (newCompanyName,))
        CompanyDataBase.commit()
        CompanyDatabaseAdd.close()
        CompanyDataBase.close()
        print("This company has now been added to the database.")

def updateTranslationInProductDatabase(ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\Python")

    ProductDataBase = productDatabase()

    #Stores the query to check if the company exists is in the database.
    CheckSKUQuery = "SELECT SKU FROM qrtable WHERE SKU = %s"
    #Stores the query to add the new data to the database.
    CheckCompanyQuery = "SELECT Company FROM qrtable WHERE Company = %s"

    UpdateQuery = "UPDATE qrtable SET translation = %s WHERE SKU = %s and Company = %s"

    #Check to see if an object already exists in the database
    SKUCheckInProductDataBase = ProductDataBase.cursor()
    SKUCheckInProductDataBase.execute(CheckSKUQuery, (ProductTuple[PositionOfProductSKU],))
    SKUCheckInProductDataBaseResult = SKUCheckInProductDataBase.fetchone()

    #Check to see if an object already exists in the database
    CompanyCheckInProductDataBase = ProductDataBase.cursor()
    CompanyCheckInProductDataBase.execute(CheckCompanyQuery, (ProductTuple[PositionOfCompanyName],))
    CompanyCheckInProductDataBaseResult = CompanyCheckInProductDataBase.fetchone()

    if SKUCheckInProductDataBaseResult and CompanyCheckInProductDataBaseResult:
        TranslationUpdate = ProductDataBase.cursor()
        TranslationUpdate.execute(UpdateQuery, (ProductTuple[PositionOfTranslation], ProductTuple[PositionOfProductSKU], ProductTuple[PositionOfCompanyName],))
        TranslationUpdate.commit()
        ProductDataBase.close()
        ProductDataBase.close()
    else:
        print(f"Unable to update database {ProductTuple[PositionOfProductSKU]} does not exist for {ProductTuple[PositionOfCompanyName]}.")
        ProductDataBase.close()
        ProductDataBase.close()
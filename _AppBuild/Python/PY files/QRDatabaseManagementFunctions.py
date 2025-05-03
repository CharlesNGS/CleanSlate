#Imported modules
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from dotenv import load_dotenv
from hashlib import sha256
import csv
import mysql.connector
import os
import qrcode

#Function to take a company and their product SKU, turn it into a hash.
def hashMaker(CompanynameForHash, ProductSKUForHash):
    preHashDetails = (CompanynameForHash+ProductSKUForHash).encode('utf-8')
    QRHash = sha256(preHashDetails).hexdigest()
    return QRHash

#Takes a hash and turns it into a complete URL
def URLMaker(QRHash):
    MyURL = "mywebsite.com/verify?hash="
    ProductURL = MyURL+QRHash
    return ProductURL

#Takes a URL and turns it into a QR code. QR Code is made into an image and saved to a variable.
def QRMaker(ProductURL):
    #Highest level of error correction and lowest QR Code version that supports enough characters for the URL
    QRParameters = qrcode.QRCode(version= 8,
                                 error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRParameters.add_data(ProductURL)
    QRParameters.make(fit=True)
    QRCode = QRParameters.make_image()
    return QRCode

#Function that runs once to see if the CSV is in order or malformed
def OrderOfProducts(ProductTuple, ProductRequirements):
    #Product requirements checks that all the columns correctly exist
    ProductTupleFields = tuple(ProductField.strip().lower() for ProductField in ProductTuple)
    if ProductRequirements.issubset(ProductTupleFields):
        CompanynamePosition = ProductTupleFields.index("companyname")
        ProductSKUPosition = ProductTupleFields.index("productsku")
        TranslationPosition = ProductTupleFields.index("translation")
        print(f"CompanynamePosition is equal to {CompanynamePosition}")
        print(f"ProductSKUPosition is equal to {ProductSKUPosition}")
        print(f"TranslationPosition is equal to {TranslationPosition}")
        return (CompanynamePosition, ProductSKUPosition, TranslationPosition)
    else:
        print("CSV is malformed. Please check that the following titles exist in the first line: Companyname, ProductSKU, Translation.")
        quit()

def AddQRToDataBase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\Python")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    QRDataBase = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    CompanyDataBase = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )

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
    QRDatabaseCheck = QRDataBase.cursor()
    QRDatabaseCheck.execute(CheckProductQuery, (QRHash,))
    QRDatabaseCheckResult = QRDatabaseCheck.fetchone()

    #If the QR code already exists
    if not CompanyDatabaseCheckResult:
        print(f"The company {ProductTuple[PositionOfCompanyName]} has not yet been setup.")
        CompanyDatabaseCheck.close()
        CompanyDataBase.close()
    #If the QR code already exists
    elif QRDatabaseCheckResult:
        print("This product has already been added to the database.")
        QRDatabaseCheck.close()
        QRDataBase.close()
        return False
    else:
        QRDatabaseAdd = QRDataBase.cursor()
        QRDatabaseAdd.execute(InsertProductQuery, (QRHash, ProductTuple[PositionOfTranslation], ProductTuple[PositionOfCompanyName], ProductTuple[PositionOfProductSKU]))
        QRDataBase.commit()
        QRDatabaseAdd.close()
        QRDataBase.close()
        return True

#Function to merge all other functions allowing them to run in order and trigger only if all information is satisfied.
def newProduct(ProductTuple):
    PositionOfCompanyName = 0
    PositionOfProductSKU = 1
    PositionOfTranslation = 2

    Companyname = ProductTuple[PositionOfCompanyName]
    ProductSKU = ProductTuple[PositionOfProductSKU]
    Translation = ProductTuple[PositionOfTranslation]
    CompanynameForHash = Companyname.strip().lower()
    ProductSKUForHash = ProductSKU.strip().lower()

    #Statement to verify all variables exist in a format that the query can use
    if CompanynameForHash and ProductSKUForHash and Translation:
        QRHash = hashMaker(CompanynameForHash, ProductSKUForHash)
        ProductURL = URLMaker(QRHash)
        QRCode = QRMaker(ProductURL)

        #Confirms the items are added to the database before saving the QR Code
        if AddQRToDataBase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
            QRCode.save(r'D:\CleanSlate\_AppBuild\Python\Referenced Files\qrcode.png')
            print("Database has been updated with the new details for this product.")
        else:
            print("Details provided could not be saved to the database. Please check the details and try again.")
            quit()
    else:
        print(f"""Missing input please check the following fields:
              Company Name: {Companyname or '[MISSING]'}
              Product SKU: {ProductSKU or '[MISSING]'}
              Translation: {Translation or '[MISSING]'}""")
        quit()

#Function to take company data and product data in bulk
def newProductCSV(CSVNewProduct):
    ProductsUnordered = True
    with open(CSVNewProduct, 'r', encoding='utf-8-sig') as csvfile:
        NewProductDetails = csv.reader(csvfile)
        for ProductLine in NewProductDetails:
            ProductTuple = tuple(ProductLine)

            ProductRequirements = {"companyname", "productsku", "translation"}

            if ProductsUnordered:
                TupleOrderOfProducts = OrderOfProducts(ProductTuple, ProductRequirements)
                PositionOfCompanyName = TupleOrderOfProducts[0]
                PositionOfProductSKU = TupleOrderOfProducts[1]
                PositionOfTranslation = TupleOrderOfProducts[2]
                ProductsUnordered = False

            elif ProductTuple and not ProductRequirements.issubset(ProductTuple):
                Companyname = ProductTuple[PositionOfCompanyName]
                ProductSKU = ProductTuple[PositionOfProductSKU]

                CompanynameForHash = Companyname.strip().lower()
                ProductSKUForHash = ProductSKU.strip().lower()

                QRHash = hashMaker(CompanynameForHash, ProductSKUForHash)
                ProductURL = URLMaker(QRHash)
                QRCode = QRMaker(ProductURL)
                if AddQRToDataBase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
                    QRCode.save(r'D:\CleanSlate\_AppBuild\Python\Referenced Files\qrcode.png')
                    print("Database has been updated with the new details for this product.")
                else:
                    print(f"Details for {ProductTuple} provided could not be saved to the database. Please check the details and try again.")
            else:
                print("All lines added to database now.")
                quit()
                    

#Function to merge all other functions allowing them to run in order for CSV files and trigger only if all information is satisfied.

def newCompany(newCompanyName):
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

def updateTranslation(ProductTuple):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"D:\CleanSlate\_AppBuild\Python\Referenced Files\Python")

    QRDataBase = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=os.getenv("MYSQLPassword"),
    database="dev_db"
    )

    #Stores the query to check if the company exists is in the database.
    CheckProductSKUQuery = "SELECT SKU FROM qrtable WHERE SKU = %s"
    #Stores the query to add the new data to the database.
    CheckCompanyNameQuery = "SELECT Company FROM qrtable WHERE Company = %s"

    #Check to see if an object already exists in the database
    ProductSKUCheck = QRDataBase.cursor()
    ProductSKUCheck.execute(CheckProductSKUQuery, (ProductTuple[PositionOfProductSKU],))
    ProductSKUCheckResult = CheckProductSKUQuery.fetchone()

    #Check to see if an object already exists in the database
    CompanyCheck = QRDataBase.cursor()
    CompanyCheck.execute(CheckCompanyNameQuery, (QRHash,))
    CompanyCheckResult = CheckCompanyNameQuery.fetchone()
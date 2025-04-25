#Imported modules
from dotenv import load_dotenv
import os
import csv
import mysql.connector
import qrcode
from hashlib import sha256

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

def AddQRToDataBase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
    #ENV used for storing the password. Not best practice just a simple way to keep the password from being hard coded.
    load_dotenv(dotenv_path=r"C:\Python\QRPasswordenv.env")

    #Database connection specifying the host address, port, user, password from ENV file and the schema to use.
    QRDataBase = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("MYSQLPassword"),
        database="dev_db"
    )


    #Stores the query to check if the hash is in the database.
    CheckQuery = "SELECT * FROM qrtable WHERE qrhash = %s"
    #Stores the query to add the new data to the database.
    InsertQuery = "INSERT INTO qrtable (qrhash, translation, Company, SKU) Values (%s, %s, %s, %s)"

    #
    QRDatabaseCheck = QRDataBase.cursor()
    QRDatabaseCheck.execute(CheckQuery, (QRHash,))
    QRDatabaseCheckResult = QRDatabaseCheck.fetchone()
    #If the QR code already exists
    if QRDatabaseCheckResult:
        print("This product has already been added to the database.")
        QRDatabaseCheck.close()
        QRDataBase.close()
        return False
    else:
        QRDatabaseAdd = QRDataBase.cursor()
        QRDatabaseAdd.execute(InsertQuery, (QRHash, ProductTuple[PositionOfTranslation], ProductTuple[PositionOfCompanyName], ProductTuple[PositionOfProductSKU]))
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
        if AddQRToDataBase(QRHash, ProductTuple, 0, 1, 2):
            QRCode.save(r'C:\Python\qrcode.png')
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

            ProductRequirements = {"Companyname", "ProductSKU", "Translation"}
            if ProductRequirements.issubset(ProductTuple) and ProductsUnordered:
                TupleOrderOfProducts = OrderOfProducts(ProductTuple, ProductRequirements)
                PositionOfCompanyName = TupleOrderOfProducts[0]
                PositionOfProductSKU = TupleOrderOfProducts[1]
                PositionOfTranslation = TupleOrderOfProducts[2]
                ProductsUnordered = False

            if ProductTuple and not ProductRequirements.issubset(ProductTuple):
                Companyname = ProductTuple[PositionOfCompanyName]
                ProductSKU = ProductTuple[PositionOfProductSKU]

                CompanynameForHash = Companyname.strip().lower()
                ProductSKUForHash = ProductSKU.strip().lower()

                QRHash = hashMaker(CompanynameForHash, ProductSKUForHash)
                ProductURL = URLMaker(QRHash)
                QRCode = QRMaker(ProductURL)
                if AddQRToDataBase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
                    QRCode.save(r'C:\Python\qrcode.png')
                    print("Database has been updated with the new details for this product.")
                else:
                    print(f"Details for {ProductTuple} provided could not be saved to the database. Please check the details and try again.")
            else:
                print("All lines added to database now.")
                quit()
                    
#Function that runs once to see if the CSV is in order or malformed
def OrderOfProducts(ProductTuple, ProductRequirements):
    if ProductRequirements.issubset(ProductTuple):
        CompanynamePosition = ProductTuple.index("Companyname")
        ProductSKUPosition = ProductTuple.index("ProductSKU")
        TranslationPosition = ProductTuple.index("Translation")
        print(f"CompanynamePosition is equal to {CompanynamePosition}")
        print(f"ProductSKUPosition is equal to {ProductSKUPosition}")
        print(f"TranslationPosition is equal to {TranslationPosition}")
        return (CompanynamePosition, ProductSKUPosition, TranslationPosition)
    else:
        print("CSV is malformed. Please check that the following titles exist in the first line: Companyname, ProductSKU, Translation.")
        quit()
#Function to merge all other functions allowing them to run in order for CSV files and trigger only if all information is satisfied.
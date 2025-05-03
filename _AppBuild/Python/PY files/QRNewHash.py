import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from QRDatabaseManagementFunctions import AddQRToDataBase
from hashlib import sha256
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
import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
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

#Function that runs once to see if the CSV is in order or malformed
def checkCSVOrderAndContents(ProductTuple, ProductRequirements):
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
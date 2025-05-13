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
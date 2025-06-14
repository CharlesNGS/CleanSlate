import sys
sys.path.insert(0, r"D:\CleanSlate\_AppBuild\Python\Imports")
from PYFiles.adminFunctions.DatabaseInteractions import addProductToProductDatabase
from PYFiles.adminFunctions.InputProcessing import checkCSVOrderAndContents, hashMaker, URLMaker, QRMaker
import csv

#Takes an input based off of a products details and creates all required components to add one single new product to a database
def singleNewProduct(ProductTuple):
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
        if addProductToProductDatabase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
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

#Takes an input based off of a products details and creates all required components to add as many new products as there are in a CSV to a database
def multipleNewProduct(CSVNewProduct):
    LineNumber = 0
    FailedCSVLines = []
    with open(CSVNewProduct, 'r', encoding='utf-8-sig') as csvfile:
        NewProductDetails = csv.reader(csvfile)
        for ProductLine in NewProductDetails:
            ProductTuple = tuple(ProductLine)
            ProductRequirements = {"companyname", "productsku", "translation"}
            LineNumber += 1

            if LineNumber == 1:
                TupleOrderOfProducts = checkCSVOrderAndContents(ProductTuple, ProductRequirements)
                PositionOfCompanyName = TupleOrderOfProducts[0]
                PositionOfProductSKU = TupleOrderOfProducts[1]
                PositionOfTranslation = TupleOrderOfProducts[2]


            elif ProductTuple and LineNumber > 1:
                Companyname = ProductTuple[PositionOfCompanyName]
                ProductSKU = ProductTuple[PositionOfProductSKU]

                CompanynameForHash = Companyname.strip().lower()
                ProductSKUForHash = ProductSKU.strip().lower()

                QRHash = hashMaker(CompanynameForHash, ProductSKUForHash)
                ProductURL = URLMaker(QRHash)
                QRCode = QRMaker(ProductURL)
                if addProductToProductDatabase(QRHash, ProductTuple, PositionOfCompanyName, PositionOfProductSKU, PositionOfTranslation):
                    QRCode.save(r'D:\CleanSlate\_AppBuild\Python\Referenced Files\qrcode.png')
                    print("Database has been updated with the new details for this product.")
                else:
                    print(f"Details for {ProductTuple} provided could not be saved to the database. Please check the details and try again.")
                    FailedCSVLines.append({"Missing Line" : ProductTuple, "Missing Line Number" : LineNumber})
            else:
                if FailedCSVLines:
                    print(f"Lines added to database excluding: {FailedCSVLines}")
                    return FailedCSVLines
                else:
                    print("All lines added to database.")
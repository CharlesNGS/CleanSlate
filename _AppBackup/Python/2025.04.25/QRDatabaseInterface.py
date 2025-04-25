from QRCreateAddToDatabase import newProduct
from QRCreateAddToDatabase import newProductCSV
from QRCreateAddToDatabase import newCompany

#Three inputs must be satisfied
DataEntry = input("Specify input: CSV or Single")
if DataEntry.lower() == "single":
    Companyname = input("Company Name")
    ProductSKU = input("Product SKU")
    Translation = input("Product Description")
    ProductTuple = (Companyname, ProductSKU, Translation)
    #Use one function to perform the tasks of generating a QR code and adding new details to the database.
    newProduct(ProductTuple)

elif DataEntry.lower() == "csv":
    CSVNewProduct = input("Please paste file path.")
    newProductCSV(CSVNewProduct)

elif DataEntry.lower() == "company":
    newCompanyName = input("Company Name")
    newCompany(newCompanyName)
else:
    print("Input needs to be one of the following CSV or Single")
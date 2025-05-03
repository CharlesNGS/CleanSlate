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
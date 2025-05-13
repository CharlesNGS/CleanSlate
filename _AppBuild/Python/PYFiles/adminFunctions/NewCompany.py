from DataBaseConnections import companyDatabase

def addCompanyToCompanyDatabase(newCompanyName):
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
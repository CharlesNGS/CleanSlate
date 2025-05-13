#Imported functions.
from QRDatabaseCheckFunctions import completeQuery

#Hash is the variable that queries the database.
QRHashInput = input("qrHash")

#Each received input runs the inported function. 
completeQuery(QRHashInput)
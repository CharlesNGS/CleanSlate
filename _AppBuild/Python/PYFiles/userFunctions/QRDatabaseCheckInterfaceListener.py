#Imported functions.
from _AppBuild.Python.PYFiles.userFunctions.QRDatabaseCheckFunctions import completeQuery

#Hash is the variable that queries the database.
QRHashInput = input("qrHash")

#Each received input runs the inported function. 
completeQuery(QRHashInput)
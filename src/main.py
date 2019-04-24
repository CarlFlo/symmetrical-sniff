from QuerieFields import querieFields
from os import system

system("cls")

qf = querieFields.QuerieFields()

for e in qf.getList():
    print(e.query, e.desc)

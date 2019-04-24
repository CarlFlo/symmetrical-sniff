from querieFields import QuerieFields

qf = QuerieFields()

for e in qf.getList():
    print(e.query, e.desc)
from .field import Field


class QuerieFields:

    def __init__(self):
        self.list = []
        _fields = """itemLabel\n
thumbnail\n
create_fromTime
…fr.o.m. en angiven tid.
"""

        lines = _fields.splitlines()

        for i in range(0, len(lines), 2):
            self.__addToList__(lines[i], lines[i + 1])

    def __addToList__(self, query, desc):
        self.list.append(Field(query, desc))

    def getList(self):
        return self.list

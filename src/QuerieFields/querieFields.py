from .field import Field


class QuerieFields:

    def __init__(self):
        self.list = []  # thumbnail\n
        lines = """itemLabel\n
create_fromTime
fr.o.m. en angiven tid.
create_fullName
av en person med angivet namn (förnamn + efternamn).
create_nameAuth
av en person med namn enligt angiven personauktoritet.
create_nameId
av en person med angiven id.
create_organization
av en angiven organisation.
mediaLicense
Hitta objekt med angiven medialicens
byline
Hitta objekt med matchande byline
serviceOrganization\n
thumbnail\n
create_organization
av en angiven organisation.
""".splitlines()

        for i in range(0, len(lines), 2):
            self.__addToList__(lines[i], lines[i + 1])

    def __addToList__(self, query, desc):
        self.list.append(Field(query, desc))

    def getList(self):
        return self.list

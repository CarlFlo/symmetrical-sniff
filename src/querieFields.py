from field import Field

class QuerieFields:

    def __init__(self):
        self.list = []
        #self.__addToList__("create_cadastralUnit","... vid en angiven fastighetsbeteckning.")
        oof = """create_cadastralUnit
…vid en angiven fastighetsbeteckning.
create_century
…under ett angivet århundrade.
create_continentName
…på en angiven kontinent (text).
create_countryName
…i ett angivet land (text).
create_county
…i ett angivet län (id).
create_countyName
…i ett angivet län (text).
create_decade
…under ett angivet årtionde.
create_firstName
…av en person med angivet förnamn.
create_fromPeriodId
…fr.o.m. en angiven historisk period (id).
create_fromPeriodName
…fr.o.m. en angiven historisk period (text).
create_fromTime
…fr.o.m. en angiven tid.
create_fullName
…av en person med angivet namn (förnamn + efternamn).
create_gender
…av en person med angivet genus.
create_municipality
…i en angiven kommun (id).
create_municipalityName
…i en angiven kommun (text).
create_name
…av en person med angivet namn.
create_nameAuth
…av en person med namn enligt angiven personauktoritet.
create_nameId
…av en person med angiven id.
create_organization
…av en angiven organisation.
create_parish
…i en angiven socken (id).
create_parishName
…i en angiven socken (text).
create_periodAuth
…under en period enligt angiven periodsauktoritet.
create_placeName
…på en angiven plats.
create_province
…på ett angivet landskap (id).
create_provinceName
…på ett angivet landskap (text).
create_surname
…av en person med angivet efternamn.
create_title
…av en person med angiven titel/befattning/tilltal.
create_toPeriodId
…fr.o.m. en angiven historisk period (id).
create_toPeriodName
…fr.o.m. en angiven historisk period (text).
create_toTime
…t.o.m. en angiven tid."""

        lines = oof.splitlines()

        for i in range(0,len(lines),2):
            self.__addToList__(lines[i],lines[i+1])
            

    def __addToList__(self, query, desc):
        self.list.append(Field(query,desc))

    def getList(self):
        return self.list
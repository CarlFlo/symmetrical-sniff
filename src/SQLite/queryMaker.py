
class QueryMaker():

    def __init__(self):
        self.list = []

    def add(self, field, content):
        self.list.append(QueryObject(field, content))

    def getFieldsAsString(self):
        pass

    def getContentAsString(self):
        pass

    # Makes query for the items database by default
    def makeQuery(self, tableName="items"):

        query = 'insert into {} ({}) values ({})'.format(tableName, self.getFieldsAsString(), self.getContentAsString())
        return query


class QueryObject:

    def __init__(self, field, query):
        self.field = field
        self.query = query

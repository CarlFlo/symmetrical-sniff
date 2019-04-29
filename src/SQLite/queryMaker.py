
class QueryMaker:

    def __init__(self):
        self.list = []

    def add(self, field, content):
        self.list.append(QueryObject(field, content))

    def getFieldsAsString(self):
        fieldsList = []
        for e in self.list:
            fieldsList.append(str(e.getField()))
        return ', '.join(fieldsList)

    def getContentAsString(self):
        contentList = []
        for e in self.list:
            contentList.append(str(e.getContent()))
        return ', '.join(contentList)

    # Makes query for the items database by default
    def makeQuery(self, tableName="items"):

        query = 'insert into {} ({}) values ({})'.format(tableName, self.getFieldsAsString(), self.getContentAsString())
        return query


class QueryObject:

    def __init__(self, field, content):
        self.field = field
        self.content = content

    def getField(self):
        return self.field

    def getContent(self):
        return self.content

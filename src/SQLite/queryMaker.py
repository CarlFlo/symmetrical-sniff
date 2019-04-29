
class QueryMaker:

    def __init__(self):
        self.list = []

    def add(self, field, content):
        self.list.append(QueryObject(field, content))

    def getFieldsAsString(self):
        fieldsList = []
        for e in self.list:
            fieldsList.append(e.getField())
        return ', '.join(fieldsList)

    def getContentAsString(self):
        contentList = []
        for e in self.list:
            contentList.append(e.getContent())
        return ', '.join(contentList)

    # Makes query for the items database by default
    def makeQuery(self, tableName="items"):

        query = 'INSERT INTO {} ({}) VALUES ({})'.format(tableName, self.getFieldsAsString(), self.getContentAsString())
        return query


class QueryObject:

    def __init__(self, field, content):

        content = str(content)  # Så att det är en string
        self.field = str(field)
        self.content = "\""+content.replace('"', "'")+"\""

    def getField(self):
        return self.field

    def getContent(self):
        return self.content

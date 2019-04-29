import sqlite3 as sql
import threading


class DB:

    def __init__(self, *args):
        if len(args) > 0:
            self._dbMakeConnection(args[0])
        else:
            raise Exception("Database: No args in constructor")

    def _dbMakeConnection(self, dbName):
        self.con = sql.connect(dbName)

        if self.con == None:
            raise Exception("Could not create/connect to database")

    def dbCloseConnection(self):
        self.con.close()

    def dbCommit(self):
        self._getConnection().commit()

    def dbCommitInThread(self):
        threading.Thread(target=self.dbCommit).start()

    def getVersion(self):
        cur = self._getCursor()
        cur.execute('SELECT SQLITE_VERSION()')

        data = cur.fetchone()[0]

        print(str.format("SQLite version: {}", data))

    def _getConnection(self):
        return self.con

    def _getCursor(self):
        return self._getConnection().cursor()

    def dbDropTable(self, tableName):
        self.dbExecute(str.format("drop table if exists {}", tableName))
        self.dbCommit()

    def dbExecute(self, query):

        cur = self._getCursor()
        try:
            cur.execute(query)
        except Exception:
            print("EXECUTE FAILED")

        return cur.fetchall()

    #####

    def dbUpdateRecord(self, newValue):
        cur = self._getCursor()
        cur.execute('UPDATE currentRecord SET record = {} where id = 1'.format(newValue))
        self.dbCommit()

    def dbGetRecord(self):
        cur = self._getCursor()
        cur.execute('SELECT record from currentRecord')
        return int(cur.fetchone()[0])

    def dbShowRecord(self):
        cur = self._getCursor()
        cur.execute('SELECT record from currentRecord')

        data = cur.fetchone()[0]

        print(data)

    def dbExecuteAndPrint(self, query):
        self._printResult(self.dbExecute(query))

    def _printResult(self, result):

        for row in result:
            finalStr = ""
            for elem in row:
                finalStr += str(elem) + ", "
            print(finalStr[:-2])

    #####

    def createTables(self):

        ### items ###
        query = """
        CREATE TABLE items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        itemId varchar(50) not null,
        itemLabel varchar(50),
        create_from Timevarchar(50),
        create_fullName varchar(50),
        create_nameAuth varchar(50),
        create_nameId varchar(50),
        create_organization varchar(50)
        )"""

        self.dbDropTable("items")
        self.dbExecute(query)

        ### currentRecord ###
        query = """
        CREATE TABLE currentRecord(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record UNSIGNED SMALLINT unique not null
        )"""

        self.dbDropTable("currentRecord")
        self.dbExecute(query)

        # Adds default value
        self.dbExecute("insert into currentRecord (record) values (0)")

        self.dbCommit()

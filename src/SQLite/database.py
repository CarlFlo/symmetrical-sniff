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
        cur = self.getCursor()
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
        except Exception as e:
            pass

        return cur.fetchall()

    #####

    def createTables(self):

        ### items ###
        query = """
        CREATE TABLE items(
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )"""

        self.dbDropTable("items")
        self.dbExecute(query)

        ### currentPage ###
        query = """
        CREATE TABLE currentPage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        onPage UNSIGNED SMALLINT unique not null
        )"""

        self.dbDropTable("currentPage")
        self.dbExecute(query)

        self.dbCommit()
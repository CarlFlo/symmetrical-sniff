import sqlite3 as sql


class MultiDatabase:
    def executeAndClose(self, query):
        conn = sql.connect("databas.db")
        conn.cursor().execute(query)
        conn.commit()
        conn.close()

    def ExecuteSetup(self):
        self.conn = sql.connect("databas.db")

    def executeQuery(self, query):
        self.conn.cursor().execute(query)

    def executeDone(self):
        self.conn.commit()
        self.conn.close()

    def setup(self):

        self.ExecuteSetup()

        query = """
        CREATE TABLE items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        itemId varchar(50) not null,
        itemLabel varchar(50),
        create_fullName varchar(50),
        create_nameAuth varchar(50),
        create_nameId varchar(50),
        create_fromTime varchar(50),
        mediaLicense varchar(50),
        byline varchar(50),
        serviceOrganization varchar(50),
        thumbnail varchar(70),
        create_organization varchar(50)
        )"""

        self.executeQuery('drop table if exists items')
        self.executeQuery(query)

        # Not used for multiprocessing
        query = """
                CREATE TABLE currentRecord(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record UNSIGNED SMALLINT unique not null
                )"""
        self.executeQuery('drop table if exists currentRecord')
        self.executeQuery(query)

        self.executeQuery('insert into currentRecord (record) values (0)')
        #

        self.executeDone()

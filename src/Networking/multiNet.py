import math
import time
from os import system
import datetime
from pathlib import Path

import requests
from SQLite import multiDatabase, queryMaker
from utils import bcolors
from multiprocessing.dummy import Pool


class MultiprocessingNetworking:

    # Multiprocessing
    tCurrentDone = 0
    tLastPrint = time.time()  # Used to limit the amount of prints that get sent to cmd
    maxPool = 4  # Keep low! Each will make a request to the server simultaneously (default 4) More does not = faster!
    updateEverySec = 2  # How the minumum wait time in sec the program will wait to print out it's progress

    # Default
    hitsPerPage = 500  # Default 500
    URL = 'http://www.kulturarvsdata.se/ksamsok/api'
    URLFields = '{}?&x-api=test&method=search&hitsPerPage={}&recordSchema=xml'.format(URL, hitsPerPage)
    query = 'itemType=foto AND thumbnailExists=j'
    # K-samsök supports JSON if given the following Accept header
    headers = {
        'Accept': 'application/json'
    }

    # Samma kod som i net.py
    def makeRequest(self, fields):

        # initial query to know how many results we get
        queryURL = '{}&query={}&fields={}&startRecord='.format(
            self.URLFields, self.query, fields)

        print("# Requesting")
        r = requests.get(queryURL, headers=self.headers)

        json = r.json()
        totalResults = json['result']['totalHits']
        requiredRequests = math.ceil(totalResults / self.hitsPerPage)

        print('# {} Requests required'.format(requiredRequests))
        # print('# {} Requests required for fields:\n{}'.format(requiredRequests, fields))
        self.threadingMaster(requiredRequests, queryURL)

    # multiprocessing
    def threadingMaster(self, rr, queryURL):
        system('title Working multiprocessing... Pool: {}'.format(self.maxPool))

        # Setup
        my_file = Path("databas.db")
        if my_file.is_file():
            print("## Remeber to remove DB file before running (databas.db) multiprocessing can't resume (yet) ##")
            input("Press Enter to continue...")
        multiDatabase.MultiDatabase().setup()

        # Gör URL:en global
        self.queryURL = queryURL
        self.rr = rr  # Request Required. Så requests som behöver göras

        indexes = range(rr + 1)
        pool = Pool(self.maxPool)
        print('# Multiprocessing starting (Pool: {})'.format(self.maxPool))
        self.startTime = time.time()
        pool.map(self.worker, indexes)  # Skapar alla jobb

        pool.close()
        pool.join()
        print('\n\n{}# Done!{}'.format(bcolors.bcolors.OKGREEN, bcolors.bcolors.ENDC))

    def worker(self, index):
        startRecord = index * self.hitsPerPage
        r = requests.get(self.queryURL + str(startRecord), headers=self.headers)
        responseJSON = r.json()

        db = multiDatabase.MultiDatabase()
        db.ExecuteSetup()

        for j, record in enumerate(responseJSON['result']['records']['record']):
            # Skapa query
            QM = queryMaker.QueryMaker()
            allGood = True

            # Itererar genom alla record's fields
            for fi, field in enumerate(record['field']):

                # Lägg till sakerna i queriet, gör en lista object etc

                content = ""
                try:
                    content = field['content']
                except:
                    allGood = False  # Something is very wrong
                    break

                # Add to query here
                QM.add(field['name'], content)

            # Något är fel med fältet så hoppa över den
            if not allGood:
                continue

            # Kör query/lägg in data
            query = QM.makeQuery()  # Skapar ett query från alla fält
            db.executeQuery(query)  # Kör queriet

        # Done with page
        db.executeDone()  # Closes the connection and commits data to DB
        self.tCurrentDone += 1

        # Displays progress after a minimum time as elapsed
        if (time.time() - self.tLastPrint) > self.updateEverySec:
            self.tLastPrint = time.time()

            proc = '%.2g' % ((self.tCurrentDone / self.rr) * 100)
            timePassed = time.time() - self.startTime
            PrettyTimePassed = str(datetime.timedelta(seconds=int(timePassed)))

            timeLeftSec = (timePassed / self.tCurrentDone) * self.rr
            PrettyTimeLeft = str(datetime.timedelta(seconds=int(timeLeftSec)))

            print('{}%\tDuration: {} | ETA: {}'.format(proc, PrettyTimePassed, PrettyTimeLeft))

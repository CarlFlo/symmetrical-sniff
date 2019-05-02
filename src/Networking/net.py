import math
import time
import json
from os import system

import requests
from SQLite import database, queryMaker
from utils import bcolors


class Networking:

    hitsPerPage = 500  # Default 500
    URL = 'http://www.kulturarvsdata.se/ksamsok/api'
    URLFields = '{}?&x-api=test&method=search&hitsPerPage={}&recordSchema=xml'.format(URL, hitsPerPage)
    query = 'itemType=foto AND thumbnailExists=j'
    # K-samsök supports JSON if given the following Accept header
    headers = {
        'Accept': 'application/json'
    }

    def __init__(self):
        self.DB = database.DB("databas.db")

    def saveJSONToFile(self, jsonData):
        with open('data.json', 'w') as json_file:
            json.dump(jsonData, json_file)

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
        self.callGenerator(requiredRequests, queryURL)

    def callGenerator(self, requiredRequests, queryURL):
        system("title Working...")
        totalSkipped = 0

        startedTime = time.time()
        for i in range(self.DB.dbGetRecord(), requiredRequests):  # Checka om den kör den sista
            recordStartTime = time.time()
            startRecord = i * self.hitsPerPage
            localSkipped = 0

            r = requests.get(queryURL + str(startRecord), headers=self.headers)
            responseJSON = r.json()

            # print(r.url)
            # self.saveJSONToFile(responseJSON)  # Save to file. Debug

            # Hämtar och går igenom alla resultat, record är en lista/array med fields
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

                # Kör query/lägg in data

                # Något är fel med fältet så hoppa över den
                if not allGood:
                    localSkipped += 1
                    continue

                query = QM.makeQuery()
                self.DB.dbExecute(query)

            # Done with page
            totalSkipped += localSkipped
            self.DB.dbUpdateRecord(i+1)  # Updates record

            # Commit to DB, and time it
            start_time = time.time()
            self.DB.dbCommit()

            # Display progress
            _commitMS = '%.2g' % ((time.time() - start_time) * 1000)  # Must be first to be accurate
            _pctDone = '%.2g' % ((i / requiredRequests) * 100)  # Bug. Gets weird when on 99%+ (1e+123) <-
            _progress = '{}/{}'.format(i, requiredRequests)
            _left = requiredRequests-i
            _skipped = localSkipped
            _tookSecInt = time.time() - recordStartTime
            _tookSec = '%.2g' % _tookSecInt
            _durationSec = int(time.time()-startedTime)
            _durationMin = '%.2g' % (_durationSec/60)
            _durationH = '%.2g' % (_durationSec/60/60)

            _estSec = _left*_tookSecInt
            _estMin = '%.2g' % (_estSec/60)
            _estH = '%.2g' % (_estSec/60/60)

            progress = "{} {}% Total skipped: {} Estemated: {} Hours, {} Min".format(_progress, _pctDone, totalSkipped, _estH, _estMin)
            system('title {}'.format(progress))

            print('{}% {} ({}). Skipped: {}. SQL: {} ms.\tThis took {} sec. Duration: {} h, {} min, {} sec'.format(_pctDone, _progress, _left, _skipped, _commitMS, _tookSec, _durationH, _durationMin, _durationSec))

        print('\n\n{}Done!{}'.format(bcolors.bcolors.OKGREEN, bcolors.bcolors.ENDC))

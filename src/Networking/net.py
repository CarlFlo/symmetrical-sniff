import math, time, json
from os import system

import requests
from SQLite import database


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

        print("Requesting")
        r = requests.get(queryURL, headers=self.headers)

        json = r.json()
        totalResults = json['result']['totalHits']
        requiredRequests = math.ceil(totalResults / self.hitsPerPage)

        print(requiredRequests, "requests required for fields:\n", fields)
        self.callGenerator(requiredRequests, queryURL)

    def callGenerator(self, requiredRequests, queryURL):

        for i in range(self.DB.dbGetRecord(), requiredRequests):  # Checka om den kör den sista
            startRecord = i * self.hitsPerPage

            r = requests.get(queryURL + str(startRecord), headers=self.headers)
            responseJSON = r.json()

            # print(r.url)
            # self.saveJSONToFile(responseJSON)  # Save to file. Debug

            # Hämtar och går igenom alla resultat, record är en lista/array med fields
            for record in responseJSON['result']['records']['record']:

                ### Skapa query

                # Itererar genom alla record's fields
                for field in record['field']:

                    ## Lägg till sakerna i queriet, gör en lista object etc

                    print(field['name'], ": ", end="", sep="")
                    try:
                        print(field['content'])
                    except:
                        print("null")

                ### Kör query/lägg in data

            # Done with page
            # Visa användaren hur mycket som är gjort
            progress = "'{}/{} {}%'".format(i, requiredRequests, ((i / requiredRequests) * 100),end="")
            print(progress)
            system("title", progress)
            self.DB.dbUpdateRecord(i)  # Updates record

            # Commit to DB, and time it
            start_time = time.time()
            self.DB.dbCommit()
            print(time.time() - start_time, " seconds to commit", sep="")

import math

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

        for i in range(requiredRequests):
            startRecord = i * self.hitsPerPage

            r = requests.get(queryURL + str(startRecord), headers=self.headers)
            responseJSON = r.json()

            ### Albin's kod
            for record in responseJSON['result']['records']['record']:
                # sometimes there are empty records and those has no fields :-(
                if not len(record) == 2:
                    continue

                item_to_yield = {}

                # some fields can appear multiply times
                # therefor we need to merge those to lists if needed
                for field in record['field']:
                    # if the field is already a list
                    if isinstance(item_to_yield.get(field['name'], False), list):
                        item_to_yield[field['name']].append(field['content'])
                    # if it's not yet a list but we found the same field name/key again
                    elif item_to_yield.get(field['name'], False):
                        item_to_yield[field['name']] = list(
                            [item_to_yield[field['name']], field['content']])
                    # default to just a regular value
                    else:
                        item_to_yield[field['name']] = field['content']

                ## Add to DB
                # self.DB.dbExecute("")

                # yield item_to_yield
            print(((i/requiredRequests) * 100), "%", sep="")
            ## Commit to DB
            # self.DB.dbCommitInThread()

import math

import requests


class Networking:
    hitsPerPage = 500
    URL = 'http://www.kulturarvsdata.se/ksamsok/api'
    URLFields = '{}?&x-api=test&method=search&hitsPerPage={}&recordSchema=xml'.format(URL, hitsPerPage)
    query = 'itemType=foto AND thumbnailExists=j'

    def __init__(self):
        pass

    def call(self, fields):
        # K-samsök supports JSON if given the following Accept header
        headers = {
            'Accept': 'application/json'
        }

        # initial query to know how many results we get
        queryURL = '{}&query={}&fields={}&startRecord='.format(
            self.URLFields, self.query, fields)
        
        print("Requesting")
        r = requests.get(queryURL, headers=headers)

        json = r.json()
        totalResults = json['result']['totalHits']
        requiredRequests = math.ceil(totalResults / 500)

        print(requiredRequests, " requests required for fields:\n", fields)

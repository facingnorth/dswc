'''
This is designed for the new Azure Marketplace Bing Search API (released Aug 2012)

Inspired by https://github.com/mlagace/Python-SimpleBing and
http://social.msdn.microsoft.com/Forums/pl-PL/windowsazuretroubleshooting/thread/450293bb-fa86-46ef-be7e-9c18dfb991ad
'''

import requests # Get from https://github.com/kennethreitz/requests
import string

class BingSearchAPI():
    bing_api = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Composite?"

    def __init__(self, key):
        self.key = key

    def replace_symbols(self, request):
        # Custom urlencoder.
        # They specifically want %27 as the quotation which is a single quote '
        # We're going to map both ' and " to %27 to make it more python-esque
        request = string.replace(request, "'", '%27')
        request = string.replace(request, '"', '%27')
        request = string.replace(request, '+', '%2b')
        request = string.replace(request, ' ', '%20')
        request = string.replace(request, ':', '%3a')
        return request

    def search(self, sources, query, params):
        ''' This function expects a dictionary of query parameters and values.
Sources and Query are mandatory fields.
Sources is required to be the first parameter.
Both Sources and Query requires single quotes surrounding it.
All parameters are case sensitive. Go figure.

For the Bing Search API schema, go to http://www.bing.com/developers/
Click on Bing Search API. Then download the Bing API Schema Guide
(which is oddly a word document file...pretty lame for a web api doc)
'''
        request = 'Sources="' + sources + '"'
        request += '&Query="' + str(query) + '"'
        for key,value in params.iteritems():
            request += '&' + key + '=' + str(value)
        request = self.bing_api + self.replace_symbols(request)

        print request
        return requests.get(request, auth=(self.key, self.key)).json


if __name__ == "__main__":
    my_key = "key"
    bing = BingSearchAPI(my_key)
    data = []


    j=0
    while len(data)<2000 :
        params = {'ImageFilters':'"Face:Face"',
                  '$format': 'json',
                  '$top': 20,
                  #'$offset':(0+j)*20
                  #'$skip':(0+j)*20
        }
        x =  bing.search('web','web',params)

        print x

        for foo in x[u'd'][u'results']:
            i=0
            for bar in foo:
                url = ""
                try:
                    url = foo['Web'][i]['Url']
                    if  "wordpress.com" in url:
                        continue
                    else:
                        print url
                    data.append(foo['Web'][i]['Url'])
                except Exception, e:
                    pass


                i+=1

        j+=1


    dataset = set(data)
    for xx in dataset:
        print xx


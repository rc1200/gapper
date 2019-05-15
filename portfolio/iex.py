#!/usr/bin/env python

# Copyright 2019-2020 iexcloud. or its affiliates. All Rights Reserved.
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import sys, os, base64, datetime, hashlib, hmac
import requests # pip install requests
import json

from decouple import config # pip install python-decouple
import pandas as pd




# ************* REQUEST VALUES *************

host = 'cloud.iexapis.com'

# access_key = config('IEX_PUBLIC_KEY')
# secret_key = config('IEX_SECRET_KEY')

access_key = 'pk_908d3547248549428866b03ba25e03e5'
secret_key = 'sk_8706ac0f72e2481995ad2fbc5d372816'


# combo to get all market data so I can shortlit based on Price
	# symbol = 'market'
	# outputType= 'ohlc'

# combo for 1 month of apple data
symbol = 'aapl'
outputType= 'chart/1m'



def sign(key, msg):
    return hmac.new(key.encode('utf-8'), msg.encode('UTF-8'), hashlib.sha256).hexdigest()

def getSignatureKey(key, dateStamp):
    kDate = sign(key, dateStamp)
    return sign(kDate, 'iex_request')

if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

# print(access_key)
# print(secret_key)


def getData(symbol, outputType):

    # since we can't pass '/' for the Ajax call, we substitue ~~ to /
    outputType = outputType.replace('**','/')


    method = 'GET'
    canonical_querystring = 'token=' + access_key
    canonical_uri = '/beta/stock/{}/{}'.format(symbol,outputType)
    endpoint = "https://" + host + canonical_uri

    t = datetime.datetime.utcnow()
    iexdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    canonical_headers = 'host:' + host + '\n' + 'x-iex-date:' + iexdate + '\n'
    signed_headers = 'host;x-iex-date'
    payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    algorithm = 'IEX-HMAC-SHA256'
    credential_scope = datestamp + '/' + 'iex_request'
    string_to_sign = algorithm + '\n' +  iexdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    signing_key = getSignatureKey(secret_key, datestamp)
    signature = hmac.new(signing_key.encode('utf-8'), (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    headers = {'x-iex-date':iexdate, 'Authorization':authorization_header}

    # ************* SEND THE REQUEST *************
    request_url = endpoint + '?' + canonical_querystring

    print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
    print('Request URL = ' + request_url)
    r = requests.get(request_url, headers=headers)

    print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
    print('Response code: %d\n' % r.status_code)
    # print(r.text)
    # print(r.json())

    return r.json()


class ShortList(object):

    def __init__(self, lowPrice, highPrice):
        self.lowPrice = lowPrice
        self.highPrice = highPrice
        self.__symbol = 'market'
        self.__outputType= 'ohlc'
        self.filteredStocks = getData(self.__symbol, self.__outputType)
        # self.df = pd.DataFrame(self.filteredStocks)
        self.df = pd.DataFrame.from_dict(self.filteredStocks, orient='index')


    def mydata (self):
        print(self.lowPrice)
        print(self.highPrice)
        # print(self.filteredStocks)
        print(self.df.head())

aaa = ShortList(1,1000)
aaa.mydata()


class getStockData(object):

    def __init__(self, symbol, outputType):
        self.symbol = symbol
        self.outputType = outputType
        self.stockJSON = getData(self.symbol, self.outputType)
        self.df = pd.DataFrame.from_dict(self.stockJSON, orient='columns')

    def df_OHLC(self):
        return self.df.loc[:,['date','open','high','low','close','volume']]

    def json_OHLC(self):
        jsondata = self.df.loc[:,['date','open','high','low','close','volume']]

        # converting dataframe back to JSON
        jsondata = jsondata.to_json(orient='records')#.replace('[[', '[{')
        return json.loads(jsondata)



# Testing Class getStockData
# mydata = getStockData('aapl', 'chart/1m')
# print(mydata.stockJSON)
# print(mydata.df)












# Load the first sheet of the JSON file into a data frame
# df = pd.DataFrame.from_dict(json, orient='columns')

# print(df)


# reduce data to OHLC
# df = df.loc[:,['date','open','high','low','close','volume']]
# print(df)


#
# dfp = pd.DataFrame.from_dict(json, orient='columns')
# dfp = dfp.loc[:,['date','open','high','low','close','volume']]
# # change index so previous
# dfp.index = dfp.index - 1
# # Rename Columns based on List
# dfp.columns =['pdate','popen','phigh','plow','pclose','pvolume']
# dfp = dfp.loc[0:]
#
# print(df.head())
# print(dfp.head())
#
# dfm = pd.merge(df, dfp, right_index=True, left_index=True)
# print(dfm)
#
# # find Gap UP
# print(dfm.loc[(dfm.open > dfm.pclose) & (dfm.open > dfm.phigh)])
# # find Gap Down
# print(dfm.loc[(dfm.open < dfm.pclose) & (dfm.open < dfm.phigh)])


# print (df.columns.values)


# reference.symbols()
# Stock("F").price()
# /stock/{symbol}/ohlc


# works
# https://cloud.iexapis.com/beta/tops?token=pk_908d3547248549428866b03ba25e03e5&symbols=aapl
# https://cloud.iexapis.com/beta/stock/aapl/quote?token=pk_908d3547248549428866b03ba25e03e5
# https://cloud.iexapis.com/beta/stock/aapl/ohlc?token=pk_908d3547248549428866b03ba25e03e5
# https://cloud.iexapis.com/beta/stock/aapl/previous/ohlc?token=pk_908d3547248549428866b03ba25e03e5

# Minute data for a specific day
# https://cloud.iexapis.com/beta/stock/aapl/chart/date/20190220?token=pk_908d3547248549428866b03ba25e03e5

# Get 1 month of data, has OHLC
# https://cloud.iexapis.com/beta/stock/aapl/chart/1m?token=pk_908d3547248549428866b03ba25e03e5

# /stock/aapl/quote/extendedPrice--  efers to the 15 minute delayed price outside normal market hours 0500 - 0930 ET and 1600 - 2000 ET. This provides pre market and post market price. This is purposefully separate from latestPrice so users can display the two prices separately.
# https://cloud.iexapis.com/beta/stock/aapl/quote/extendedPrice?token=pk_908d3547248549428866b03ba25e03e5

# https://cloud.iexapis.com/beta/stock/aapl/quote?filter=extendedPrice,latestPrice?token=pk_908d3547248549428866b03ba25e03e5
# get the average volume + other cool stuff
#https://cloud.iexapis.com/beta/stock/aapl/stats?token=pk_908d3547248549428866b03ba25e03e5



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
# see example of decouple where you use a .env file in the root to store your credentials
    # SECRET_KEY = config('SECRET_KEY')
    # DEBUG = config('DEBUG', cast=bool)
# the SECRET_KEY and DEBUG defined in the .env file something like:
    # SECRET_KEY=3izb^ryglj(bvrjb2_y1fZvcnbky#358_l6-nn#i8fkug4mmz!
    # DEBUG=True
# As well in Heroku, you can got o Settings tab click on the Reveal Config Vars 
# https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html
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

    '''
    usage example: 
        get a list of stocks between the low and high price -> myStockList = ShortList(50, 200)

    Methods: *** currently not working as this requires a paid subscription

    '''
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

# aaa = ShortList(1,1000)
# aaa.mydata()


class getStockData(object):

    '''
    usage example: 
        get 1 month of data (per day) -> ABC = getStockData('aapl', 'chart/1m')

    Methods:
        ABC.df_OHLC() - output as Dataframe Open, High, Low, Close
        ie.
          date    open    high     low   close    volume
            0   2019-11-29  266.60  268.00  265.90  267.25  11654363
            1   2019-12-02  267.27  268.25  263.45  264.16  23693550
            2   2019-12-03  258.31  259.53  256.29  259.45  29377268

        ABC.json_OHLC() - output as JSON string  Open, High, Low, Close
    
        [{'date': '2019-11-29', 'open': 266.6, 'high': 268.0, 'low': 265.9, 'close': 267.25, 'volume': 11654363}, 
        {'date': '2019-12-02', 'open': 267.27, 'high': 268.25, 'low': 263.45, 'close': 264.16, 'volume': 23693550}]

    '''

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

    def is_Up_Down_day(self, row):
        if row['open'] > row['close']:
            return 'down'
        elif row['open'] < row['close']:
            return 'up'
        else:
            return 'same'


    def open_vs_close(self):


        #  ???? how does this respond for the current day if it is still -1 for current day


        # row to check if the current day was an "up" or "down" day based on the open and close
        self.df['prevDayType'] = self.df.apply(lambda row: self.is_Up_Down_day(row), axis=1)
        current = self.df.iloc[-1:]
        prev = self.df.iloc[-2:-1]
        currentPrice = 300

        # > prev high
            # if prev up then continue
            # if prev down then shock
                
        # < prev low
            # if prev up then shock
            # if prev down then continue

        print(self.df)
        print('current')
        print(current)
        print('prev')
        print(prev)      


        # self.df['new'] = self.df.apply(lambda row: is_Up_Down_day(row), axis=1)
        # print(self.df)
        # return a,b,c



# ---------------------------- following code works
# Store JSON data into dataframe
# df = pd.DataFrame.from_dict(json, orient='index')
# # extract the dictionary value from the dataframe column 'close' as a list then feed into a new dataframe
# df2 = pd.DataFrame(df['close'].values.tolist())
# # set the index to be the same value as the original Dataframe
# df2.set_index(df.index, inplace =True)
# # combine both datafrmae based on the index value (stock symbol)
# df = pd.concat([df, df2], axis=1, join_axes=[df.index])
# # drop the columns you don't need
# df.drop(['open','close','time'], axis=1, inplace=True)
# # rename column
# df.rename(columns={'price': 'closing_price'}, inplace=True)
# # filter based on range - create new dataframe to store value
# df_filtered = df[(df.closing_price >= 10) & (df.closing_price <= 33.33)]
# -------------------------



# df.drop('open', axis=1, inplace=True)
# # Testing Class getStockData
# # mydata = getStockData('aapl', 'chart/1m')
# # print(mydata.stockJSON)
# # print(mydata.df)

# from pandas.io.json import json_normalize
# df = pd.DataFrame.from_dict(json, orient='index')
# df['ddd'] = df['close'].astype(str)
# df['eee'] = df['ddd'].str.extract('time...(\d+)', expand=True)


# or other option is to have dataframe converted to dictionary then use the map
# ... ie see http://cmdlinetips.com/2018/01/how-to-add-a-new-column-to-using-a-dictionary-in-pandas-data-frame/







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



import requests
import datetime
import json
import pandas as pd
from secretstuff import tosapikey

# symbol = 'SPX'
# # define endpoint
# endpoint = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory'

# # define payload
# payload = {'apikey': tosapikey,
#             'periodType' : 'month',
#             'period' : '1',
#             'frequencyType' : 'daily',
#             'frequency' : '1',
#             'endDate' : '1576818000000',
#             'startDate' : '1575176400000',
#             'needExtendedHoursData' : 'false'}

# content = requests.get(url = endpoint, params = payload)
# data = content.json()

# print('data---------------------------')
# print(data)
# print('data---------------------------')

            

def getTOSData(symbol, endpointType, periodType, period, frequencyType, frequency, endDate, startDate, needExtendedHoursData):

    endpoint = f'https://api.tdameritrade.com/v1/marketdata/{symbol}/{endpointType}'
    
    payload = {'apikey': tosapikey,
                'periodType' : periodType,
                'period' : period,
                'frequencyType' : frequencyType,
                'frequency' : frequency,
                'endDate' : endDate,
                'startDate' : startDate,
                'needExtendedHoursData' : needExtendedHoursData}

    content = requests.get(url = endpoint, params = payload)
    data = content.json()

    return data




class getTOSStockData(object):
    
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



class getTOSStockData(object):

    def __init__(self, symbol, endpointType, periodType, period, frequencyType, frequency, endDate, startDate, needExtendedHoursData):
        self.symbol = symbol
        self.endpointType = endpointType
        self.periodType = periodType
        self.period = period
        self.frequencyType = frequencyType
        self.frequency = frequency
        self.endDate = endDate
        self.startDate = startDate
        self.needExtendedHoursData = needExtendedHoursData

        self.stockJSON = getTOSData(self.symbol, self.endpointType, self.periodType, self.period, 
            self.frequencyType, self.frequency, self.endDate, self.startDate, self.needExtendedHoursData)['candles']
        self.df = pd.DataFrame.from_dict(self.stockJSON, orient='columns')
        self.df['humanTime'] = self.df.apply(lambda row: self.epochToReadableTime(row), axis=1)
        
    def epochToReadableTime (self, row):
        # convert epoch To Readable Time
        dt = row['datetime']
        dts = str(dt)[:-5] # convert to string and remove last 5 characters ie. 1576476000000.0 => 1576476000
        intdts = int(dts) # convert back to integer
        return datetime.datetime.fromtimestamp(intdts)

    # def updateDF (self):
    #     self.df['humanTime'] = self.df.apply(lambda row: self.epochToReadableTime(row), axis=1)
    #     print(self.df)

    def df_OHLC(self):
        return self.df.loc[:,['humanTime','open','high','low','close','volume']]


    def json_OHLC(self):
        jsondata = self.df.loc[:,['datetime','open','high','low','close','volume']]

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


b = getTOSStockData('SPX', 'pricehistory', 'month', '1', 'daily', '1','1576818000000','1575176400000','false')

# print(b.stockJSON)
print(b.df)
print(b.df_OHLC())
print(b.json_OHLC())
    
# a = getTOSData('SPX', 'pricehistory', 'month', '1', 'daily', '1','1576818000000','1575176400000','false')
# print(a)



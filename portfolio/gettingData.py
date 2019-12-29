from iex import getData, getStockData


a = getStockData('aapl', 'chart/1m')
print(a.df_OHLC())

# print(getData('aapl', 'chart/1m'))
from iex import getStockData, getData
from secretstuff import access_key, secret_key


a = getStockData('aapl', 'chart/1m')
print(a.df_OHLC())
# print(a.json_OHLC())
latestPrice = getData('aapl', 'quote/latestPrice')
print(a.open_vs_close(latestPrice))


# a = getStockData('spx', 'chart/1m')
# print(a.df_OHLC())


# https://cloud.iexapis.com/beta/stock/aapl/quote/latestPrice?token=pk_908d3547248549428866b03ba25e03e5


# myStockList = ShortList(50, 200)
# print(myStockList.mydata())
# myStockList.mydata()

# print(getData('aapl', 'chart/1m'))

print(access_key)
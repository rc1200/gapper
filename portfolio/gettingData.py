from iex import getStockData, ShortList



a = getStockData('aapl', 'chart/1m')
print(a.df_OHLC())
# print(a.json_OHLC())
print(a.open_vs_close())



# myStockList = ShortList(50, 200)
# print(myStockList.mydata())
# myStockList.mydata()

# print(getData('aapl', 'chart/1m'))
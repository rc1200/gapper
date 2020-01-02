import requests


import datetime


tm = 1576818000000
strtm = int(str(tm)[:-3])
print(strtm)
a = datetime.datetime.fromtimestamp(int(str(tm)[:-3]))
print(a)
# 1576818000000
# 1347517370

# print( 1576818000000 - 1000)

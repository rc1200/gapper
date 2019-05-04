import pandas as pd

# create dictionary data
city = {'id': [3, 2, 1, 1],
        'city': ['Toronto', 'Oakville', 'Mississauga', 'Mississauga'],
        'postal': ['1111', '2222', '3333', '4444']}


# create dataframe manually from Dictionary/List
dfc = pd.DataFrame(city)
print(dfc)


# order by ID ascending, postal descending order
dfc = dfc.sort_values(by=['id', 'postal'], ascending=[True, False])
print(dfc)


# do the above in 1 step
dfc = pd.DataFrame(city).sort_values(by=['id', 'postal'], ascending=[True, False])
print(dfc)


# create similar as above but using list and doing a zip then Define the columns manually
# ie Sandwich getting smushed, then take a bit is a set
my_zip = zip([3, 2, 1, 1],
             ['Toronto', 'Oakville', 'Mississauga', 'Mississauga'],
             ['1111', '2222', '3333', '4444'])
print('my_zip -----------------', my_zip)
city = list(my_zip)
print('my_zip turned to list -', city)

# vs  list of tuples
my_list_of_tuples = [(3, 'Toronto', '1111'),
                     (2, 'Oakville', '2222'),
                     (1, 'Mississauga', '3333'),
                     (1, 'Mississauga', '4444')]
print('my_list_of_tuples -----', my_list_of_tuples)
city2 = my_list_of_tuples


# single command to set df
dfc = pd.DataFrame(city2, columns=['cityID', 'cityName', 'cityPostal']).sort_values(by=['cityID', 'cityPostal'], ascending=[True, False])
print('\nUsing list of tuples' + '\n' * 2, dfc)


# single command to set df
dfc = pd.DataFrame(city, columns=['cityID', 'cityName', 'cityPostal']).sort_values(by=['cityID', 'cityPostal'], ascending=[True, False])
print('\nUsing list that was ziped then converted back to a list' + '\n' * 2, dfc)


# set index
dfc.set_index('cityID')
print(dfc)


# since the index should be unique, this should not be the index but the city ID
dfc.reset_index
print(dfc)


# since the index should be unique, this should not be the index but the city ID
dfc.rename(columns={'cityID': 'cityNumber'}, inplace=True)
print(dfc)


# reset Index to be anal and inplace to commit the change
dfc.reset_index(drop=True, inplace=True)
print(dfc)


zone = {'zoneID': [1, 2, 3],
        'zoneName': ['M', 'O', 'T']}


dfz = pd.DataFrame(zone)

dfmerge = pd.merge(dfc, dfz, left_on='cityNumber', right_on='zoneID')
print(dfmerge)


# Filtering
print(dfmerge.loc[dfmerge.zoneID < 3])
# Filtering with & and Or
print(dfmerge.loc[(dfmerge.zoneID < 3) & ((dfmerge.zoneID == 1) | (dfmerge.zoneID == 2))])

# 2nd and 3rd rows then specific columns by Name
print(dfmerge.loc[1:2, ['cityName', 'zoneID']])
# 1st and 3rd column, and specific column name
print(dfmerge.loc[[0, 2], ['cityName', 'zoneID']])

# using iloc to get rows/columns by numeric value
print(dfmerge.iloc[[0, 2], 1:4])

print(dfmerge)

# delete column zoneName
dfmerge.drop('zoneName', axis=1, inplace=True)
print(dfmerge)

# delete multiple columns
dfmerge.drop(['zoneID', 'cityPostal'], axis=1, inplace=True)
print(dfmerge)

# delete row by index number
dfmerge.drop([3], axis=0, inplace=True)
print(dfmerge)

# delete non sequential rows by index number
dfmerge.drop([0, 2], axis=0, inplace=True)
print(dfmerge)

df2Data = {'cityNumber': [1, 1, 1, 1, 2, 2, 3, 3],
           'cityName': ['Mississauga', 'Mississauga', 'Mississauga', 'Mississauga', 'Oakville', 'Oakville', 'Toronto', 'Toronto']}

df2 = pd.DataFrame(df2Data)
print('df2\n', df2)

# append and sort by index... NOTEICE the duplicate Index Number 1
dfmerge = dfmerge.append(df2).sort_index()
print(dfmerge)

# merge but this time ignore the index
dfmerge = dfmerge.append(df2, ignore_index=True)
print(dfmerge)

# drop based on filter
# stroe the index
indexNames = dfmerge.loc[(dfmerge.cityNumber > 1) | (dfmerge.cityNumber > 2)].index
print(indexNames)
dfmerge.drop(indexNames, inplace=True)
print(dfmerge)
dfmerge.reset_index(drop=True, inplace=True)
print(dfmerge)


# set New index based on List
origIndex = list(dfmerge.index)
print(origIndex)
newIndex = list(map(lambda x: x * 2, origIndex))
dfmerge.index = newIndex
print(dfmerge)


# add column
# random ID
import random
randIDList1 = {'randID_1': [random.randint(0, 9) for x in range(9)]}
randIDList2 = {'randID_2': [random.randint(0, 9) for x in range(9)]}
print(randIDList1)
pdrand1 = pd.DataFrame(randIDList1)
pdrand2 = pd.DataFrame(randIDList2)
print(pdrand1)

# results if you don't reset the index
print(pd.concat([dfmerge, pdrand1], axis=1))
# join should work as well

dfmerge.reset_index(drop=True, inplace=True)
pdrand1.reset_index(drop=True, inplace=True)
pdrand2.reset_index(drop=True, inplace=True)

# results after dropping index
dfmerge = pd.concat([dfmerge, pdrand1, pdrand2], axis=1)
print(dfmerge)

# using group by to get some stats
print(dfmerge.groupby(['randID_1']).count())
print(dfmerge.groupby(['cityName', 'randID_2']).count())
dfcount = dfmerge.groupby(['cityName', 'randID_2']).count()
dfcount.index
print(dfcount)


dfcount.columns = ['a', 'b']
dfcount.rename(columns={'cityName': 'aa'}, inplace=True)
print(dfcount)


# convert to list
df_list_all = dfmerge.values.tolist()
df_list_multi_fields = dfmerge[['cityName', 'randID_1']].values.tolist()
df_list_city = dfmerge.cityName.tolist()

print(df_list_all, df_list_city, df_list_multi_fields)

help(pd.Series.loc)


# read from excel
# I/O
# Read and Write to CSV

# >>> pd.read_csv('file.csv', header=None, nrows=5)
# >>> pd.to_csv('myDataFrame.csv')

# Read multiple sheets from the same file

# >>> xlsx = pd.ExcelFile('file.xls')
# >>> df = pd.read_excel(xlsx,  'Sheet1')

# Read and Write to Excel

# >>> pd.read_excel('file.xlsx')
# >>> pd.to_excel('dir/myDataFrame.xlsx',  sheet_name='Sheet1')


# define the file to read
xls = pd.ExcelFile('C:/Users/rc/Google Drive/corporation/2019/2019 Corporate expenses.xlsx')
# assign the excel to dataframe, and choose the tab name
df = pd.read_excel(xls, 'Credit Card')
# df = df.loc[:, ['Date', 'Type', 'amount']]

print(df.groupby(['Type'])['amount', 'credit'].agg('sum'))

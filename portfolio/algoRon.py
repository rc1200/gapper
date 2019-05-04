# Libraries Included:
# Numpy, Scipy, Scikit, Pandas
import pandas as pd

city = [{'cityId': 1, 'cityName': 'Amsterdam'},
        {'cityId': 2, 'cityName': 'London'},
        {'cityId': 3, 'cityName': 'Toronto'},
        {'cityId': 4, 'cityName': 'Tokio'},
        {'cityId': 5, 'cityName': 'Frankfurt'},
        {'cityId': 6, 'cityName': 'Zurich'},
        {'cityId': 7, 'cityName': 'Berlin'},
        {'cityId': 8, 'cityName': 'Belgrade'}]

flights = [
    {'flight': 1, 'Departure': 1, 'Destination': 3, 'time': 1234567, 'plane_type': 'Boeing 737'},
    {'flight': 2, 'Departure': 5, 'Destination': 6, 'time': 4356789, 'plane_type': 'Airbus 231'},
    {'flight': 3, 'Departure': 3, 'Destination': 2, 'time': 8456782, 'plane_type': 'SSJ 900'},
    {'flight': 4, 'Departure': 3, 'Destination': 7, 'time': 4765432, 'plane_type': 'Boeing 737'},
    {'flight': 5, 'Departure': 1, 'Destination': 5, 'time': 3456789, 'plane_type': 'SSJ 900'},
    {'flight': 6, 'Departure': 4, 'Destination': 6, 'time': 3456789, 'plane_type': 'Boeing 737'},
    {'flight': 7, 'Departure': 4, 'Destination': 8, 'time': 3456786, 'plane_type': 'Airbus 231 '}]

# store in dataframe and set City as the index
dfCity = pd.DataFrame(city).set_index('cityId')
# store flights in dataframe and sort by Time asc order
dfSortedFlights = pd.DataFrame(flights).sort_values(by='time', ascending=True)


# recursive function to get the cities you can fly from based of the initial qualifying flights
def showDeparture(level, initialCityId, curCityId, dfFlight, dfCity):
    initialLevel = level
    if initialCityId == curCityId:
        print('\t' * initialLevel, dfCity.loc[curCityId, 'cityName'])

    for index, a in dfFlight.iterrows():
        nextLevel = initialLevel
        if a['Departure'] == curCityId:
            nextLevel += 1
            departFlightId.append(a['flight'])
            # print ('\t'*nextLevel, a['flight'], a['Departure'], a['Destination'], dfCity.loc[a['Destination'],'cityName']) # easier to debug with this line
            print('\t' * nextLevel, dfCity.loc[a['Destination'], 'cityName'])

            showDeparture(nextLevel, FlyFromCityID, a['Destination'], dfSortedFlights, dfCity)


# print (dfCity)
# print (dfSortedFlights)

FlyFromCityID = 1
departFlightId = []
print('----- result for Output:1 where the the first city ID  = {} ----- \n'.format(FlyFromCityID))
showDeparture(0, FlyFromCityID, FlyFromCityID, dfSortedFlights, dfCity)

print('\n----- result for Output:2  -----\n')

# convert the list that contains all the flights to a dataframe
dfFlights = pd.DataFrame({'flight': departFlightId})
dfFlights.set_index('flight')

# create a subset dataframe to store the flight and plane_type to be merged
dfPlaneType = dfSortedFlights[['flight', 'plane_type']].set_index('flight')

# Dataframe to join the above 2 dataframes on Key field Flight
dfMerge = pd.merge(dfFlights, dfPlaneType, on='flight')
print(dfMerge.groupby('plane_type').size())





def def_1_val():
    for x in range(2, 6):
        print(x)
    return x


def def_list():
    a = [x for x in range (1,5)]
    print (a)
    return a

print ('return value ', def_1_val())
def_list()

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def jsonReturn(self):
    my_dict = {'name': self.name}
    return my_dict

  def test1(self):
    print("class method test1, Hey test", self.name, self.age )


p1 = Person("John", 36)
print (p1)
print (p1.name)
print (p1.age)
print (p1.jsonReturn())



import pandas as pd

# city = [{'cityId': 1, 'cityName': 'Amsterdam'},
#         {'cityId': 2, 'cityName': 'London'},
#         {'cityId': 3, 'cityName': 'Toronto'},
#         {'cityId': 4, 'cityName': 'Tokio'},
#         {'cityId': 5, 'cityName': 'Frankfurt'},
#         {'cityId': 6, 'cityName': 'Zurich'},
#         {'cityId': 7, 'cityName': 'Berlin'},
#         {'cityId': 8, 'cityName': 'Belgrade'}]
#
# # store in dataframe and set City as the index
# dfCity = pd.DataFrame(city).set_index('cityId')
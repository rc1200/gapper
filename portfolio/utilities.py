



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
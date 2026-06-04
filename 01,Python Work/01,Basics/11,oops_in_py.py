'''
# Creating class,
class Car: # Class is like a template
  name = ""
  color = "red" # class attributes
  price = ""
  speed = "350 KMH"
  
  # '__init__()' function executes whenever an object is created.
  def __init__(self, _name, _color, _price, _speed):
    self.name, self.color, self.price, self.speed = _name, _color, _price, _speed
    print(f"{_name} object is created")
  
  def getInfo(self):
    print(f"Name: {self.name},\nColor: {self.color},\nPrice: {self.price}, \nSpeed: {self.speed}")
 # We use '@staticmethod' because we do not want to use the 'self' parameter as no attributes are being used inside the 'getSpeed()' function.
  @staticmethod
  def getSpeed():
    print("Speed is not known")

# Creating an object
# 1st object named ferrari
ferrari = Car("Ferrari" , "blue", "Rs.20,000,000", "Not known") # Car() is a class & ferrari is an object

# ferrari.color, ferrari.name, ferrari.price = "ferrari" , "blue", "Rs.20,000,000" # instance attributes

ferrari.getInfo() # This function call converts to 'Car.getInfo(ferrari)', so an argumemt is passed

ferrari.getSpeed() # This function call also converts to 'Car.getSpeed(ferrari)', so an argument is passed, if we do not want to use the self parameter as argument, so we have mark the function as '@staticmethod' method in the class.

# Another method of creating object using '__init__()' function or also called as  constructor.
# 2nd object name lamborghini
lamborghini = Car("Lamborghini", "purple", "Rs. 30,000,000", "350 KMH")
lamborghini.getInfo()


# PROBLEMS
#PB-1, Calculator class
# Creating class
import math

class Calculator:
  def __init__(self, _name):
    print(f"{_name} object is created")
  
  def square(self,_num):
    sqr = _num*_num
    print(f"Square of a given number is: {sqr}")
  def cube(self, _num):
    cb = _num*_num*_num
    print(f"Cube of a given number is: {cb}")
  def sqrrt(self, _num):
    sqt = math.sqrt(_num)
    print(f"Square root of a given number is: {sqt}")
  @staticmethod
  def greet():
    print("Hello there!")

# Creating object
function = input("What functionality you want:\nSquaring, \nCubing, \nSquare root")
n = int(input("Enter a number: "))
if(function.capitalize() == "Squaring"):
  Square = Calculator("Square")
  Square.greet()
  Square.square(n)
elif(function.capitalize() == "Cubing"):
  Cube = Calculator("Cube")
  Cube.greet()
  Cube.cube(n)
elif(function.capitalize() == "Square root"):
  Sqrt = Calculator("Square root")
  Sqrt.greet()
  Sqrt.sqrrt(n)
else:
  print("Invalid selection")
'''






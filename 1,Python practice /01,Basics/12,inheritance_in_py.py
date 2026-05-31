class Bike:
    @property # '@property' decorator makes the function to be 
    # callable as a property of an object, instead of as a function.
    def getColor(self): # 'Getter' method
        return self.color
    
    # '.setter' method always used along with '@property' decorator
    @getColor.setter # 'Setter' method
    def setColor(self, value):
        self.color = value

class Car(Bike): # 'Car' inherited the properties from parent class 'Bike'.
    name = "Lamborghini"

    @classmethod # '@classmethod' pass the value of class attribute even 
    # the instance attribute is declared.
    def getName(cls):
        print(cls.name)

    

lambo = Car()
lambo.name = "McLaren"
lambo.color = "Cyan"

lambo.getName() # For '@classmethod'

print(lambo.getColor) # For '@property' decorator

lambo.setColor = "Purple" # Calls the '.setter' method
print(lambo.getColor)


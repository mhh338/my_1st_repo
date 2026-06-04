'''
age = int(input("Enter your age: "))

if(age>18):
  print(f"User age is {age}")
elif(age<18):
  print(f"User age is {age}")
else:
  print("User is 18 years old")
  
# PROBLEMS
#PB-1, Find geatest number
num1 = int(input("Enter the number: "))
num2 = int(input("Enter the number: "))
num3 = int(input("Enter the number: "))
num4 = int(input("Enter the number: "))

# Making of list is extra
nums = [num1, num2, num3, num4]
print(nums)

if(num1 > num2 and num1 > num3 and num1 > num4):
 print(f"{num1} is the greatest number of all.")
elif(num1 < num2 and num1 < num3 and num1 < num4):
  print(f"{num4} is the greatest number of all.")
elif(num2 > num1 and num2 > num3 and num2 > num4):
  print(f"{num2} is the greatest number of all.")
else:
  print(f"{num3} is the greatest number of all.")
  
  
# PB-2, Check either the student is failed or passed

sub1 = int(input("Enter marks of subject 1: "))
sub2 = int(input("Enter marks of subject 2: "))
sub3 = int(input("Enter marks of subject 3: "))

totpercent = 40
minpercent = 33
totmarks = (sub1 + sub2 + sub3)/300 * 100

if(totmarks >= totpercent and all(sub >= minpercent for sub in [sub1, sub2, sub3])):
 print("Student has passed the examination")
 # if(min(sub1, sub2, sub3) >= minpercent):
else:
 print("Student Failed the examination")

# PB-3, Detecting spam messages
while True:
  comnt = input("Enter your Comment: ")
  keywords = ["money", "buy now", "lot of money", "subscribe this" , "click this"]
  if any(words in comnt.lower() for words in keywords):
   print("This is a spam!")
  else:
   print(comnt)
    
  restart = input("\nDo you want to run again (y/n): ")
  if(restart.lower() == "n"):
    print("program ends!")
    break

#PB-4, Number of characters in username
while True:
  username = input("Enter your username: ")

  if(len(username.replace(" ", "")) >= 10):
   print("username is composed of 10 characters")
  else:
   print("username is less than 10 characters")
  restart = input("\nDo you want to run again (y/n): ")
  if (restart.lower() == "n"):
   print("program ends")
   break

# PB-5, Finfing name in the list
while True:
  list = ["Ali", "Ahmad", "Zeeshan", "Haider", "Azmat", "Waasay", "Abrar", "Farhan", "Shahid"]

  name = input("Enter the name: ")
  if (name.capitalize() in list):
    print(f"{name.capitalize()} is included in the list.")
  else:
    print(f"{name.capitalize()} is not in the list.")
  
  restart = input("\nDo you want to run again (y/n): ")
  if(restart.lower() == "n"):
   print("program ends")
   break

# PB-6, Grade calculator
while True:
  numbers = int(input("Enter the student's numbers: "))

  if (numbers <= 100 and numbers >= 90):
   print("Student got grade \"EX\"")
  
  elif(numbers < 90 and numbers >=80):
   print("Student got grade \"A\"")
  
  elif(numbers < 80 and numbers >=70):
   print("Student got grade \"B\"")
  
  elif(numbers < 70 and numbers >=60):
   print("Student got grade \"C\"")
  
  elif(numbers < 60 and numbers >=50):
   print("Student got grade \"D\"")
  
  elif(numbers < 50):
   print("Student FAILED to pass the examination!")

  else:
   print("Enter valid numbers!")
  
  restart = input("\nDo you want to run again (y/n): ")
  if(restart.lower() == "n"):
   print("program ends")
   break
  if(restart.lower() != "n" and restart.lower() != "y"):
   print("Incorrect option")
   break
 '''
 
# PB-7, 
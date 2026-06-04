'''
# range(start, stop, step-size) is used to make sequence of numbers. 
i = range(0, 7) # or range(7)
for n in i:
 pass # pass is used to do nothing without it program throws an error.
 
# PB-1, Multiplication table of given number

num = int(input("Enter any number: "))
l = range(101)

for mul in l:
  res = num * mul
  print(f"{num} × {mul} = {res}")
 
 # PB-2, Greetings to names starts with 'S'
l =["Ahmad", "shahid", "Maaz", "Shariq", "Shakir"]
for name in l:
  if(name[0].capitalize() == "S"):
   print(f"Greetings {name.capitalize()}")

# PB-3, Problem-1 using while loop
num = int(input("Enter any number: "))
i = 0
while (i <= 100):
  mul = num * i
  print(mul)
  i = i+1

# PB-4, Finding a numher is prime or nothing
n = int(input("Enter any number: "))
num = n%2
print(num)
print(type(num))
if (num != 0):
  print(f"The given number {n} is prime")
else:
  print(f"The given number {n} is not prime")

# PB-6, Factorial of number
num = int(input("Enter any number: "))
l = range(num)
a = 1
for n in l:
  a = a * (n + 1)
  print(a)
print(f"The factorial of {num} is {a}")

# PB-7, Star pattern
n = 3 
r = range(1,n+1)
for item in r:
  if (item == 1):
    a = print("   * ")
  elif(item == 2):
    a = print(" ***")
  else:
    a = print("*****")
'''


  


'''
#PB-1, Function to find max number
list = []
n = int(input("What should be the length of the list: "))
i = 1
while (i <= n):
  num = int(input("Enter a number: "))
  list.append(num)
  i = i+1
def maxnum(list):
  res = max(list)
  return res

a = maxnum(list)
print("The greatest number of all is: ", a)

# PB-3, To print two statements in 1 line
'end = ""' is used to continue printing statements in same line.
l = [2, 4, 6, 57, 47, 24, 5]
print("Maximum number is: ", max(l), end=" ")
print("Minimum number is: ", min(l))

# PB-4, Recurssive sum of natural numbers
n = 1 
num = int(input("Upto which number do hou wantbto calculate the sum: "))
def sumnum(n):
  if(n <= num):
    return (n + sumnum(n+1))
  else:
    return 0
res = sumnum(n)
print("Your sum is: ", res)

# PB-6, Removing a word from list & stripping the words in the list.
list = [" banana     ", "   melon", "kiwi   ", "  apple  ", "  cherry "]
word = input("Enter any word from the list: ").lower()
def rmword(_word):
  print(f"Unstripped list: {list}")
  if any(w.strip() == word for w in list):
    slist = [wd.strip() for wd in list]
    slist.remove(word)
    print(f"Stripped list: {slist}")
  else:
    print(f"The word {word.lower()} is not in the list.")
rmword(word)
'''





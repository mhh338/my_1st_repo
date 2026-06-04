# Dictionaries in Python
dict = {
"name" : "Ali",
"age": 20
}
edict = {} # empty dictionary
print(type(edict))
print(dict["name"])
dict.update({"name": "Umar"})
print(dict["name"])
print(dict.items())
print(dict.keys())
print(dict.values())

# Sets in Python
st = {1, 4, 4, 3, 7, 66, 876, 4, 5 ,1}
print(st)
est = set() # empty set
print(type(est))
st.add(11)
print(st)
print(len(st))
st.remove(876)
print(st)
st.clear()
print(st)

st1 = {4, 67, 4, 8, 1, 3}
st2 = {5, 7, 4, 0, 12, 3, 8}

# Union of sets
un = st1.union(st2)
print(un)

# Intersection of sets
inter = st1.intersection(st2)
print(inter)

# PROBLEMS
# PB-1, Worda translation dictionary
words = {
  "chalna" : "to walk",
  "khana" : "to eat",
  "talwaar" : "sword"
}

word = input("Enter the word: ")
print(words[word])

# PB-2, Input unique numbers
numset = set()
n = int(input("Enter the number: "))
numset.add(n)
n = int(input("Enter the number: "))
numset.add(n)
n = int(input("Enter the number: "))
numset.add(n)
n = int(input("Enter the number: "))
numset.add(n)
n = int(input("Enter the number: "))
numset.add(n)
n = int(input("Enter the number: "))
numset.add(n)
n = int(input("Enter the number: "))
numset.add(n)
n = int(input("Enter the number: "))
numset.add(n)
print(numset)

# PB-3, Same value having different types
st = {2, 18, "18", 72}
print(st)

# PB-4, Length of the set
s = set()
s.add(2)
s.add(2.5)
s.add("3")

print(s, len(s))

# PB-5, Dictionary for 4 persons
dict4 = {}
key = input("Enter your name: ")
value = input("Enter your favourite language: ")
dict4.update({key : value})
key = input("Enter your name: ")
value = input("Enter your favourite language: ")
dict4.update({key : value})
key = input("Enter your name: ")
value = input("Enter your favourite language: ")
dict4.update({key : value})
key = input("Enter your name: ")
value = input("Enter your favourite language: ")
dict4.update({key : value})
print(dict4)

# PB-6, Changing values of list inside a set
s = {1, 23, "Ali", 6.4, [2, 4]}
# Values of list cannot be changed due to 2 reasons, 1st, list cannot be added inside the set because lists are mutable whereas sets are immutable, 2nd, sets are unordered and there is no indexing in sets.


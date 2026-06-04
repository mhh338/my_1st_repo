# Lists are mutable
ls = [34, "melon", 5.6, True]
print(ls)
ls.append(5)
print(ls)
ls.pop(1)
print(ls)
ls.insert(1, "strawberry")
print(ls)
print(ls[1:3])

# Tuples are immutable like strings
tp = (3, "green", 56.7, False)
print(tp)

# finding element in the tuple
print("green" in tp)
print(34 in tp)

# unpacking of the tuple into individual variables
a, b, c, d = tp 
print(a, b, c, d)

print(len(tp))

# PRACTICE PROBLEMS

# PB-1, Fruits list
# fruits = []
# f1 = input("Enter 1st fruit name: ")
# fruits.append(f1)
# f2 = input("Enter 2nd fruit name: ")
# fruits.append(f2)
# f3 = input("Enter 3rd fruit name: ")
# fruits.append(f3)
# f4 = input("Enter 4th fruit name: ")
# fruits.append(f4)
# f5 = input("Enter 5th fruit name: ")
# fruits.append(f5)
# f6 = input("Enter 6th fruit name: ")
# fruits.append(f6)
# f7 = input("Enter 7th fruit name: ")
# fruits.append(f7)
# print(fruits)

# PB-2, Sorted students marks
# marks = []
# m1 = int(input("Enter 1st student's marks: "))
# marks.append(m1)
# m2 = int(input("Enter 2nd student's marks: "))
# marks.append(m2)
# m3 = int(input("Enter 3rd student's marks: "))
# marks.append(m3)
# m4 = int(input("Enter 4th student's marks: "))
# marks.append(m4)
# m5 = int(input("Enter 5th student's marks: "))
# marks.append(m5)
# m6 = int(input("Enter 6th student's marks: "))
# marks.append(m6)
# marks.sort()
# print(marks)

# PB-3, Checking item assignment in tuple
# tp[1] = "red" # Cannot assign item in tuple.

# PB-4, Summing numbers of list
num = [2, 43, 7, 8]
print(sum(num))

#PB-5, Counting zeros in the tuple
a = (2, 0, 40, 2, 0, 0000, 10, 0, 302)
print(a.count(0))
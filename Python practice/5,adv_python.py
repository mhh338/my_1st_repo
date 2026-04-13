# from typing import List, Tuple, Dict
import random


# # 1, WALRUS OPERATOR
# # traditional way
# user_input = input("Do you want to continue (y/n): ")
# if(user_input.lower() == "n"):
#     print("Program ends!(printed with \'traditional\' method)")

# # using walrus operator
# if((user_input := input("Do you want to continue (y/n): ")).lower() == "n"):
#     print("Program ends!(printed with \'walrus\' operator.)")

# # 2, TYPE HINTS
# # variables types are defined as ':' operator
# # and string return type is defined by '->' operator
# age: str = input("Enter your age: ")

# def getAge(_age) -> str:
#     if(int(_age) > 18):
#         print("Eligible")
#     else:
#         print("Not Eligible")

# getAge(age)


# # 3, AVANCE TYPE HNTS
# # for tuples, lists and dictionary types we have to import these libraries from 'typing'

# #list
# names: List[str] = ["Ali", "Ahmad", "Shahzain"]

# #tuple
# ages: Tuple[int] = (22, 32, 25)

# #dictionary
# persons: Dict[str, int] = {"Ali" : 22, "Ahmad" : 32, "Shahzain" : 25}

# print(f"Names: {names}, \nAges: {ages}, \nPersons: {persons}")


# 4, MATCH CASE
# like a 'switch' statement in Js
# mkwrds = "Apple Banana Melon Strawberry"
# words = mkwrds.split(" ")
# wrd = random.choice(words)

# wrd_input = input("Enter any word from the list: ")

# def checkWrd(_wrd_input) -> str:
#     match _wrd_input:
#         case _wrd_input if _wrd_input.capitalize() == wrd:
#             return "Congratulations, You Win!"
#         case _:
#             return "Try Again!"

# print(checkWrd(wrd_input))



# num = random.randint(1,20)
# user_input = int(input("Enter any number: "))

# def checkNum(_user_input) -> str:
#     match _user_input:
#         case _user_input if _user_input == num:
#             return "Winner!"
#         case _:
#             return "Try Again!"

# print(checkNum(user_input))


# Extra 'join()' method
# l = ["apple", "banana", "melon", "grapes", "strawberry"]
# res = " or ".join(l)
# print(res)

# rep = input("Enter a fruit name: ")
# apprep = input("Do you want to append or replace a name in list with it (a/r): ")

# with open("file.txt", "r") as f:
#     text = f.read()
# with open("file.txt", "w") as f:
#     if(apprep.lower() == "a"):
#         res = res + " or " + rep
#         f.write(res)
#         print(res)
#     elif(apprep.lower() == "r"):
#         whtfrt = input("Enter fruit name from the list to replace: ")
#         ans = text.replace(whtfrt, rep)
#         f.write(ans)
#         print(ans)
#     else:
#         print("Invalid selection")
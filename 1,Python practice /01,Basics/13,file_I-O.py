# import os
# print(os.getcwd(), os.listdir())
'''
# 1. Manually create the file in the virtual memory
file_content = """banana
melon
apple"""

with open("file.txt", "w") as f:
    f.write(file_content)

# 2. Now you can read it normally
with open("file.txt", "r") as f:
    text = f.read(2) # 'read()' method without argument reads all file content and with argument reads tge content of the file upto that character number.
    line1 = f.readline() # 'readline()' method without argument reads 1st line on calling 1st time in the program, 2nd line on calling 2nd time in the program, so on and with argument read upto that cbaracter number in that line.
    line2 = f.readline()
    print("File Content: ", text, "\nFirst line:", line1.strip(), "\nSecond line: ", line2)


# PB-1, Finding word in the poem
poem = """
Twinkle twinkle little star,
how I wonder what you are.
"""
# Creating file in the virtual memory
with open("poem.txt", "w") as p:
  p.write(poem)

# Reading the created file from the virtual memory.
with open("poem.txt", "r") as p:
  text = p.read()
  if ("twinkle" in text.lower()):
    print("The poem contain the \"twinkle\" word.")
  else:
    print("The word \"twinkle\" not in the poem.")


# PB-2, High score recorder
import random
hscore = ""
def game(_start, _stop):
  res = random.randint(_start, _stop)
  return res


# Creating file in virtual memory
with open("Hi-score.txt", "w") as hs:
   hs.write(hscore)

# Reading the file
   while True:
     start = int(input("Enter start number: "))
     stop = int(input("Enter end number: "))
     hscore = str(game(start, stop))
     print("Random number: ", hscore)
     with open("Hi-score.txt", "r") as hs:
       text = hs.read()
       hs.seek(0) # As after 'read()' method the cursor stays at end of the text, the 'seek(0)' method brings the cursor to very behinning of the text. With '0' in the argument it brings cursor to 0th index of the text.
       if(text == "" or int(text) < int(hscore)):
         with open("Hi-score.txt", "w") as hs:
           hs.write(hscore)
           #hs.seek(0)
           print(f"Updated hi-score is: {hscore}")
       else:
        lhscore  = hs.read()
        print(f"Hi-score is: {lhscore}")
     restart = input("Do you want to run again (y/n): ")
     if(restart.lower() == "n"):
       print("Program ends")
       break
'''





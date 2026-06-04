import pyjokes
import os 

joke=pyjokes.get_joke()
print(joke)

dir_path = '/' # diectory path
cont = os.listdir(dir_path)
for items in cont:
  print(items)

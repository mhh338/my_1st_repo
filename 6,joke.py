import pyttsx3
# import pyjokes

# joke = pyjokes.get_joke()
# print(joke)
# pyttsx3.speak(joke)

while True:
    inp = input("Enter any sentence: ")
    def read(_inp):
        pyttsx3.speak(_inp)
    
    read(inp)
    pyttsx3.speak("Do you want to run again")
    restart = input("Do you want to run again (y/n): ")
    
    if (restart.lower() == "n"):
        print("Program Ends!")
        pyttsx3.speak("See you next time")
        break

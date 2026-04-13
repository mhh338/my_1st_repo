import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(_text):
    engine.say(_text)
    engine.runAndWait()

def processCmd(_cmd):
    if "open google" in _cmd.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in _cmd.lower():
        webbrowser.open("https://youtube.com")


if __name__ == "__main__":
    while True:
        speak("Initializing...")
        # Listening wake word 'Jarvis'
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        print("Recognizing...")

        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening!")
                audio = r.listen(source, timeout=1.5, phrase_time_limit=1)
            wakeWrd = r.recognize_google(audio)
            print(wakeWrd)
            if(wakeWrd.lower() == "jarvis"):
                speak("ya")
                # Listening commandSphinx
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCmd(command)      
        except Exception as e:
            print("Error; {0}".format(e))
import speech_recognition as sr
import webbrowser
import pyttsx3

# recognizer = sr.Recognizer()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def processCmd(_cmd):
    if "open google" in _cmd.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in _cmd.lower():
        webbrowser.open("https://youtube.com")


if __name__ == "__main__":
    speak("Initializing...")
    while True:
        # Listening wake word 'Jarvis'
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing...")

        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening!")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            wakeWrd = r.recognize_google(audio) 
            print(wakeWrd)
            if wakeWrd.lower() == "jarvis":
                # speak("ya")
                print("ya bef")
                speak("Yes sir, Jarvis is active.")
                print("ya aft")
                # Listening commandSphinx
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCmd(command)      
        except Exception as e:
            print("Error; {0}".format(e))


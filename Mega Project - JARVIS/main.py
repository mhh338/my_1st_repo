import speech_recognition as sr
import webbrowser
import pyttsx3
import webLinks
import requests
from google import genai
import os
from dotenv import load_dotenv

# recognizer = sr.Recognizer()
# newsapi = "1527e5c5e8dc426c88d064613f41aaef"


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def aiHandler(_cmd):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        client = genai.Client(api_key=api_key)
        chat = client.chats.create(model="gemini-3-flash-preview")

        user_question = _cmd
        response = chat.send_message(user_question)
        print("Gemini:", response.text)
        return response


def processCmd(_cmd):
    # 1st method of opening links
    # if "google" in _cmd.lower():
    #     print(_cmd)
    #     webbrowser.open(webLinks.links["google"])
    # elif "youtube" in _cmd.lower():
    #     print(_cmd)
    #     webbrowser.open(webLinks.links["youtube"])
    # elif "piano" in _cmd.lower():
    #     print(_cmd)
    #     webbrowser.open(webLinks.links["piano"])
    # elif "my github" in _cmd.lower():
    #     print(_cmd)
    #     webbrowser.open(webLinks.links["github"])
    # elif "commands" in _cmd.lower():
    #     speak("you can search for youtube, google, piano and git hub")

    # 2nd method of opening links
    if _cmd.lower().startswith("open"):
        print(_cmd)
        destination = _cmd.lower().split(" ")[-1]
        print(destination)
        lnk = webLinks.links[destination]
        webbrowser.open(lnk)
    elif "options" in _cmd.lower():
        print(_cmd)
        speak("you can search for youtube, google, piano and git hub")

    # elif "news" in _cmd.lower():
    #     req = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
    #     if req.status_code == 200:
    #         # Parse the JSON response
    #         data = req.json()

    #         # Extracting articles
    #         articles = data.get('articles', [])

    #         # Speak the headlines
    #         for article in articles:
    #             speak(article['title'])

    else:
        # Let GEMINI handle the request
        output = aiHandler(_cmd)
        speak(output)


if __name__ == "__main__":
    speak("Initializing...")
    # speak("my-git-hub")
    while True:
        # Listening wake word 'Jarvis'
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing...")

        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening!")
                speak("I'm listening")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            wakeWrd = r.recognize_google(audio) 
            print(wakeWrd)
            if "jarvis" in wakeWrd.lower(): 
                # speak("ya")
                speak("Yes sir, Jarvis is active.")
                # Listening commandSphinx
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=2)
                    command = r.recognize_google(audio)
                    processCmd(command)
            if(wakeWrd.lower() == "go to sleep"):
                speak("ok sir, see you next time")
                break      
        except Exception as e:
            print("Error; {0}".format(e))


import os
import requests
import pyttsx3
import speech_recognition as sr

from datetime import datetime
from random import choice
from pprint import pprint
from dotenv import load_dotenv

from functions.os_ops import open_calculator, open_terminal, open_notepad
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia

load_dotenv()

USERNAME = os.getenv('USER')
BOTNAME = os.getenv('BOTNAME')

opening_text = [
    "Cool, I'm on it.",
    "Okay, I'm working on it.",
    "Just a second.",
]

engine = pyttsx3.init()
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)


def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")

    speak(f"I am {BOTNAME}. How may I assist you?")


def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-au')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night, take care!")
            else:
                speak('Have a good day!')
            exit()
    except Exception:
        query = 'None'

    return query


if __name__ == '__main__':
    greet_user()

    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open terminal' in query:
            open_terminal()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia,?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube,?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('What do you want to search on Google,?')
            query = take_user_input().lower()
            search_on_google(query)

        elif 'joke' in query:
            speak(f"Hope you like this one")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you,")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen.")
            pprint(advice)

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines,")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

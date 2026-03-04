import speech_recognition as sr
import pyttsx3
import webbrowser
import random
import os
from pywinauto import Application
import winreg
#currently I'm working on optimisation and updating libraries
#perhaps the imports will even expend in their amounts 

#Configuration, change the example paths to your needs
VOICE_RESPONSES = ['sure', 'of course', 'no problem', 'one second', 'ok']

APP_PATHS = {
    "vs": r"D:\Microsoft VS Code\Code.exe",
    "python": r"D:\pycharm\PyCharm Community Edition 2025.1.3\bin\pycharm64.exe"
}

URLS = {
    "chess": "https://www.chess.com/home",
    "gpt": "https://chat.openai.com/",
    "github": "https://github.com/",
    "youtube": "https://www.youtube.com/",
    "music": "https://soundcloud.com/discover"
}

#assistant itself
class Assistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.app = Application(backend='uia')
        self.set_voice()

#customise the voice
    def set_voice(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 0.5)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as mic:
            self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = self.recognizer.listen(mic)
            return self.recognizer.recognize_google(audio).lower()

    def run(self):
        while True:
            try:
                command = self.listen()
                print(f"Command: {command}")
                self.handle_command(command)
            except sr.UnknownValueError:
                print("Didn't catch that. Listening again...")
                continue

    def handle_command(self, command):
        handler = COMMANDS.get(command)
        if handler:
            self.speak(random.choice(VOICE_RESPONSES))
            handler(self)
        else:
            self.speak("Command not recognized")

COMMANDS = {}

def command(name):
    def decorator(func):
        COMMANDS[name] = func
        return func
    return decorator
    
#block with commands. command("something") 
#means you can say it in microphone and the assistant will do it

@command("hello")
def say_hello(assistant):
    assistant.speak("Hi there!")

@command("goodbye")
def exit_program(assistant):
    assistant.speak("Goodbye!")
    exit(0)

@command("open chess")
def open_chess(assistant):
    webbrowser.open(URLS["chess"])

@command("open gpt")
def open_gpt(assistant):
    webbrowser.open(URLS["gpt"])

@command("open youtube")
def open_youtube(assistant):
    webbrowser.open(URLS["youtube"])

@command("open github")
def open_git(assistant):
    webbrowser.open(URLS["github"])

@command("open vs")
def open_vs(assistant):
    assistant.app.start(APP_PATHS["vs"])

@command("open python")
def open_python(assistant):
    assistant.app.start(APP_PATHS["python"])

@command("music")
def music(assistant):
    webbrowser.open(URLS["music"])

#start
if __name__ == "__main__":
    Assistant().run()
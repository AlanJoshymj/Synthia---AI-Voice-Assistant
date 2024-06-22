import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5.QtCore import QThread
import speech_recognition as sr
import os
import time
import webbrowser
import openai
import datetime
import random
import numpy as np
import pyttsx3
import playsound
import pyautogui
from config import apikey

from jarvisMainGUI1 import Ui_Dialog

chatStr = ""
engine = pyttsx3.init()

def say(text):
    ui.updateMoviesDynamically("speaking")
    engine.say(text)
    engine.runAndWait()


def chat(query):
    global chatStr
    ui.terminalPrint(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\n Synthia: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    translated_response = response["choices"][0]["text"]
    chatStr += f"{translated_response}\n"
    say(translated_response)


def open_notepad():
    os.system("notepad.exe")

def open_camera():
    os.system("start microsoft.windows.camera:")

def search_google(query):
    query = query.replace("search in google", "").strip()
    webbrowser.open(f"https://www.google.com/search?q={query}")

def write_to_notepad(text):
    open_notepad()  # Open Notepad
    # Give some time for Notepad to open
    time.sleep(1)
    # Set focus to Notepad
    pyautogui.click(x=10, y=10)
    # Type the specified text
    pyautogui.write(text)

def generate_mail(job_title, company_name):
    mail = f"Subject: Job Application for {job_title}\n"
    mail += f"Dear Hiring Manager,\n\n"
    mail += f"I am writing to express my strong interest in the {job_title} position at {company_name}. I believe that my skills and experience make me a strong candidate for this role.\n\n"
    mail += f"I have attached my resume for your review. Please feel free to contact me at your convenience to discuss further. Thank you for considering my application.\n\n"
    mail += f"Sincerely,\nYour Name"

    return mail

class jarvisMain(QThread):
    def __init__(self):
        super(jarvisMain, self).__init__()

    def run(self):
        self.runJarvis()

    def commands(self):
        ui.updateMoviesDynamically("listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                ui.terminalPrint("Recognizing...")
                query = r.recognize_google(audio, language="en-in")
                ui.terminalPrint(f"User said: {query}")
                return query
            except Exception as e:
                return "Please Repeat"

    def runJarvis(self):
        ui.terminalPrint('Welcome to Synthia A.I')
        say("Welcome Back my Friend")
        while True:
            query = self.commands()
            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                     ["google", "https://www.google.com"]]
            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])

            if "play music" in query:
                musicPath = r"C:\Users\Alexander Binny\Documents\mainGUI\nightchanges.mp3"
                try:
                    playsound.playsound(musicPath)
                except Exception as e:
                    print(f"An error occurred while playing the music: {str(e)}")

            elif "the time" in query:
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                say(f"Sir time is {hour} hours and {min} minutes")

            elif "open facetime".lower() in query.lower():
                os.system(f"open /System/Applications/FaceTime.app")

            elif "open pass".lower() in query.lower():
                os.system(f"open /Applications/Passky.app")

            elif "the date" in query.lower():
                current_date = datetime.datetime.now().strftime("%B %d, %Y")
                say(f"Today's date is {current_date}")

            elif "open notepad" in query.lower():
                open_notepad()

            elif "search in google" in query.lower():
                search_query = query.lower().replace("search in google", "").strip()
                search_google(search_query)

            elif "open camera" in query.lower():
                open_camera()

            elif "write this in notepad" in query.lower():
                text_to_write = query.lower().replace("write this in notepad", "").strip()
                write_to_notepad(text_to_write)

            elif "write a mail" in query.lower():
                say("Sure, please specify the job title and the company name for the mail.")
                job_title = self.commands()
                company_name = self.commands()
                mail_text = generate_mail(job_title, company_name)
                write_to_notepad(mail_text)
                say("I have written the mail in Notepad.")

            elif " amaljoseph Exit".lower() in query.lower():
                say("Goodbye! Exiting Synthia")
                exit()

            elif "reset chat".lower() in query.lower():
                chatStr = ""

            elif any(greeting in query.lower() for greeting in ["how are you", "how's it going", "how are you doing"]):
                say("I'm just a computer program, but thanks for asking!")

            else:
                ui.terminalPrint("Chatting...")
                chat(query)

startExecution = jarvisMain()

class guiOfJarvis(QWidget):
    def __init__(self):
        super(guiOfJarvis, self).__init__()
        self.jarvisUi = Ui_Dialog()
        self.jarvisUi.setupUi(self)
        self.runAllMovies()

        self.jarvisUi.exitbutton.clicked.connect(self.close)

    def runAllMovies(self):
        self.jarvisUi.reactorMovie = QtGui.QMovie("C:\\Users\\Alexander Binny\\Downloads\\robotsconcept_ga.gif")
        self.jarvisUi.arcLabel.setMovie(self.jarvisUi.reactorMovie)
        self.jarvisUi.reactorMovie.start()

        self.jarvisUi.speakingMovie = QtGui.QMovie("C:\\Users\\Alexander Binny\\Downloads\\alexa-amazon.gif")
        self.jarvisUi.speaking.setMovie(self.jarvisUi.speakingMovie)
        self.jarvisUi.speakingMovie.start()

        self.jarvisUi.listeningMovie = QtGui.QMovie("C:\\Users\\Alexander Binny\\Downloads\\Voice Recording Animation.gif")
        self.jarvisUi.listening.setMovie(self.jarvisUi.listeningMovie)
        self.jarvisUi.listeningMovie.start()

        self.jarvisUi.sleepingMovie = QtGui.QMovie("C:\\Users\\Alexander Binny\\Downloads\\Artificial Intelligence design.gif")
        self.jarvisUi.sleep.setMovie(self.jarvisUi.sleepingMovie)
        self.jarvisUi.sleepingMovie.start()

        startExecution.start()

    def updateMoviesDynamically(self, state):
        if state=="listening":
            self.jarvisUi.listening.raise_()
            self.jarvisUi.speaking.hide()
            self.jarvisUi.sleep.hide()
            self.jarvisUi.listening.show()
        elif state=="speaking":
            self.jarvisUi.speaking.raise_()
            self.jarvisUi.listening.hide()
            self.jarvisUi.sleep.hide()
            self.jarvisUi.speaking.show()
        elif state=="sleeping":
            self.jarvisUi.sleep.raise_()
            self.jarvisUi.listening.hide()
            self.jarvisUi.sleep.hide()
            self.jarvisUi.sleep.show()

    def terminalPrint(self, text):
        self.jarvisUi.terminaloutputbox.appendPlainText(text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = guiOfJarvis()
    ui.show()
    sys.exit(app.exec_())
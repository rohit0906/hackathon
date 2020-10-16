from django.shortcuts import render
from django.http import HttpResponse

import random
import playsound
import os
import time
import webbrowser
import bs4 as bs
import urllib.request
from gtts import gTTS
import pyautogui

global voice_data
# Create your views here.
def home(request):
    return render(request,'home.html',{'name':'Ratnesh'})
def func(request):
    voice_data=request.POST['input']
    respond(voice_data)
    return render(request,'home.html',{'name':voice_data})


class person:
    name = ''
    def setName(self, name):
        self.name = name
class asis:
    name = ''
    def setName(self, name):
        self.name = name
person_obj = person()
asis_obj = asis()
asis_obj.name = 'kiki'


def there_exists(terms,voice_data):
    for term in terms:
        if term in voice_data:
            return True

def engine_speak(audio_string):
    tts=gTTS(text=audio_string,lang='en')
    r=random.randint(1,10000000)
    audio_file='audio-'+str(r)+".mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)

def respond(voice_data):
    #  greeting
    global person_obj,asis_obj
    if there_exists(['hey','hi','hello'],voice_data):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        engine_speak(greet)
    #  name
    elif there_exists(["your name should be"],voice_data):
        asis_name = voice_data.split("be")[-1].strip()
        engine_speak("okay, i will remember that my name is " + asis_name)
        asis_obj.setName(asis_name)
    elif there_exists(["what is your name","what's your name","tell me your name"],voice_data):
        if person_obj.name:
            engine_speak("My name is Alexa")
        else:
            engine_speak("my name is Alexis. what's your name?")
    elif there_exists(["my name is"],voice_data):
        person_name = voice_data.split("is")[-1].strip()
        engine_speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name) # remember name in person object
    #  greeting
    elif there_exists(["how are you","how are you doing"],voice_data):
        engine_speak(f"I'm very well, thanks for asking {person_obj.name}")
    #  time
    elif there_exists(["what's the time","tell me the time","what time is it"],voice_data):
        time = time.ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        engine_speak(time)
    #  search google
    elif there_exists(["search for","search","find for me"],voice_data) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url ='https://www.google.com/search?source=hp&ei=mzSKXrigErWL4-EPpe6NyA4&q='+search_term+"&oq=coro&gs_lcp=CgZwc3ktYWIQAxgCMgUIABCDATIFCAAQgwEyAggAMgUIABCDATIFCAAQgwEyBQgAEIMBMgIIADIFCAAQgwEyAggAMgIIADoOCAAQ6gIQtAIQmgEQ5QJKFQgXEhEwZzI1NGcyNzhnMjI1ZzIyNUoNCBgSCTBnMWcxZzFnMVC5QFjbQ2C2WGgDcAB4AIABsQKIAekIkgEHMC4yLjIuMZgBAKABAaoBB2d3cy13aXqwAQY&sclient=psy-ab"
        webbrowser.get().open(url)
        engine_speak(f'Here is what I found for  {search_term}  on google')
    # : search youtube
    elif there_exists(["youtube"],voice_data):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        engine_speak(f'Here is what I found for {search_term} on youtube')
    # weather
    elif there_exists(["weather"],voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q="+search_term+"&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        engine_speak("Here is what I found for on google")
    # game 
    elif there_exists(["game"],voice_data):
        voice_data = record_audio("choose among rock,paper or scissor")
        moves=["rock", "paper", "scissor"]
        cmove=random.choice(moves)
        pmove=voice_data
        

        engine_speak("I chose " + cmove)
        engine_speak("You chose " + pmove)
        #engine_speak("hi")
        if pmove==cmove:
            engine_speak("the match is draw")
        elif pmove== "rock" and cmove== "scissor":
            engine_speak("Player wins")
        elif pmove== "rock" and cmove== "paper":
            engine_speak("Computer wins")
        elif pmove== "paper" and cmove== "rock":
            engine_speak("Player wins")
        elif pmove== "paper" and cmove== "scissor":
            engine_speak("Computer wins")
        elif pmove== "scissor" and cmove== "paper":
            engine_speak("Player wins")
        elif pmove== "scissor" and cmove== "rock":
            engine_speak("Computer wins")
    # toss a coin
    elif there_exists(["toss","flip","coin"],voice_data):
        moves=["head", "tails"]   
        cmove=random.choice(moves)
        engine_speak("The computer chose " + cmove)
    # calc
    elif there_exists(["plus","minus","multiply","divide","power","+","-","*","/"],voice_data):
        opr = voice_data.split()[1]

        if opr == '+':
            engine_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
        elif opr == '-':
            engine_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
        elif opr == 'multiply':
            engine_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
        elif opr == 'divide':
            engine_speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
        elif opr == 'power':
            engine_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
        else:
            engine_speak("Wrong Operator")
    # screenshot
    elif there_exists(["capture","my screen","screenshot"],voice_data):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('media/images/capture.png')     
    # to search wikipedia for definition
    elif there_exists(["definition of"],voice_data):
        definition=voice_data.split("definition of")[-1][1:]
        #definition=record_audio("what do you need the definition of")
        url=urllib.request.urlopen('https://en.wikipedia.org/wiki/'+definition)
        soup=bs.BeautifulSoup(url,'lxml')
        definitions=[]
        for paragraph in soup.find_all('p'):
            definitions.append(str(paragraph.text))
        if definitions:
            if definitions[1]:
                engine_speak ('Here is what i found ') 
                engine_speak(definitions[1])
            elif definitions[2]:
                engine_speak('here is what i found '+definitions[2])
            else:
                engine_speak('im sorry i could not find that definition, please try a web search')
                
        else:
                engine_speak("im sorry i could not find the definition for "+definition)
    # exit
    elif there_exists(["exit", "quit", "goodbye"],voice_data):
        engine_speak("going offline")
        exit() 
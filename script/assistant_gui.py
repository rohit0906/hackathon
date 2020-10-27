if True:
    #from tkinter import *
    import speech_recognition as sr
    from time import ctime
    import webbrowser,time
    import playsound
    import os
    import random,pyttsx3,pyautogui
    from gtts import gTTS
    import bs4 as bs
    import urllib.request
    from . import send_msg
    import wikipedia,requests
    import wolframalpha
    from .calender.create_event import create_event

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
def record_audio(ask=""):
    r=sr.Recognizer()
    if ask:
        engine_speak(ask)
    else:
        engine_speak("speak now")
    with sr.Microphone() as source:
        audio = r.listen(source,5,5) 
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            engine_speak('I did not get that')
        except sr.RequestError:
            engine_speak('Sorry, the service is down') 
        return voice_data.lower()
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
    #creating events in google calender
    elif there_exists(["event"],voice_data):
        '''summary="Event",description="This is a tutorial example of automating google calendar with python"
        ,date=datetime.now().day,month=datetime.now().month,year=datetime.now().year,
        hour=datetime.now().hour,minute=datetime.now().minute,duration=1'''
        create_event()
    # messaging services
    elif there_exists(["whatsapp"],voice_data):
        send_msg.send_whatsapp("this is an alert whatsapp")
    elif there_exists(["sms","message"],voice_data):
        send_msg.send_sms("this is an alert sms") 
    elif there_exists(["email","gmail","mail"],voice_data):
        send_msg.send_mail("this is an alert mail") 
    elif there_exists(["alert","danger","police"],voice_data):
        send_msg.send_whatsapp("this is an alert mail") 
        send_msg.send_sms("this is an alert mail")
        send_msg.send_mail("this is an alert mail")  
    #News services
    elif there_exists(["tell me news","news","todays news","todays headline"],voice_data):
        main_url = " https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=9bd432aa4f3a4d028182f037fcfb6b18"
        open_bbc_page = requests.get(main_url).json() 
        article = open_bbc_page["articles"] 
        results = [] 
        for ar in article: 
            results.append(ar["title"]) 
        for i in range(5): 
            engine_speak(results[i]) 
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
    #  time
    elif there_exists(["what's the time","tell me the time","what time is it","time"],voice_data):
        t = time.ctime().split(" ")[3].split(":")[0:2]
        if t[0] == "00":
            hours = '12'
        else:
            hours = t[0]
        minutes = t[1]
        if int(hours)>=12:
            t = f'the time is {int(hours)-12} hours {minutes} minutes  PM'
        else:
            t = f'the time is {int(hours)-12} hours {minutes} minutes AM'
        engine_speak(t)
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
            engine_speak(str(int(voice_data.split()[0]) + int(voice_data.split()[2])))
        elif opr == '-':
            engine_speak(str((int(voice_data.split()[0]) - int(voice_data.split()[2])))
        elif opr == 'multiply':
            engine_speak(str(int(voice_data.split()[0]) * int(voice_data.split()[2])))
        elif opr == 'divide':
            engine_speak(str(int(voice_data.split()[0]) / int(voice_data.split()[2])))
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
    #Opening normal applications
    elif there_exists(["open"],voice_data):
        app = voice_data.split("open")[-1]
        try:
            os.system(f"start {app}")
            engine_speak(f"Opening {app}")
        except:
            engine_speak(f"{app} not found")
    # exit
    elif there_exists(["exit", "quit", "goodbye"],voice_data):
        engine_speak("going offline")
        exit() 
    #Random queries with wolframaplha 
    else:
        engine_speak('Searching...')
        try:
            try:
                app_id = "4GEY95-8G7P978E7W" 
                client = wolframalpha.Client(app_id) 
                res = client.query(voice_data) 
                answer = next(res.results).text
                engine_speak('Got it.')
                engine_speak('WOLFRAM-ALPHA says - '+answer)
            except:
                results = wikipedia.summary(voice_data, sentences=2)
                engine_speak('Got it.')
                engine_speak('WIKIPEDIA says - '+results)
        
        except:
            webbrowser.open('www.google.com')
def engine_speak(audio_string):
    tts=gTTS(text=audio_string,lang='en',slow=False)
    filename=str(random.randint(1,100110))+"welcome.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

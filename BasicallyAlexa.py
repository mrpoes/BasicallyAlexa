from googlesearch import search
import speech_recognition as sr
import webbrowser
import pywhatkit
import threading
import playsound
import datetime
import pyttsx3
import time

with open('config/botname.txt','r') as f:
    botname = str(f.read().lower())

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

ttsFilter = [
    f'{botname} '
    'could you ',
    'will you',
    'can you ',
    'please ',
]

timerFilter = [
    'set the timer for ',
    'set a timer for ',
    'set timer for ',
    'timer for ',
]

timeFormats = {
    'seconds' : 1,
    'second'  : 1,
    'minutes' : 60,
    'minute'  : 60,
    'hours'   : 3600,
    'hour'    : 3600,
}

def tts(audio):
    engine.say(audio)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            r.pause_threshold = 1
            audio = r.listen(source,timeout=1)
            query = r.recognize_google(audio, language='en-US').lower()

        except: # Couldn't listen
            return None

    if f'{botname}' in query:
        query = query.replace(f'{botname} ','')
        for filter in ttsFilter:
            query = query.replace(filter,'')
        return query
    
    else: # Botname not in speech to text
        return None

# def formatTime(query):
#     splitQuery = query.split(' ')
#     duration = float(splitQuery[0])
#     finalTime = duration * timeFormats[splitQuery[1]]
    
#     return finalTime

def formatTime(query):
    amt = ''
    allwords = query.split(' ')

    for word in query:
        try:
            word = int(word)
            amt += str(word)
        except:
            pass

    for word in allwords:
        for form in timeFormats.keys():
            if word in form:
                timeFormat = form

    return (float(amt) * timeFormats[str(timeFormat)],f'{amt} {timeFormat}')

def setTimer(formattedTime:str):
    time.sleep(formattedTime[0])
    playsound.playsound('config/timer.mp3',block=False)

def getLocalTime():
    return datetime.datetime.now().strftime('%I %M %p')

def playSong(query):
    try:
        query = query.replace('play ','')
        tts(f'Playing Song {query}')
        pywhatkit.playonyt(query)
        
    except: # Couldn't play song
        pass

def googleSearch(query):
    try:
        for res in search(query,lang='en'):
            print(f'Query: {query} | Result: {res}')
            tts(f'This is what I found for {query}')
            return webbrowser.open_new_tab(res)
    except: # Couldn't find result?
        pass
            

def main():
    tts(f'Hello! {botname} is listening.')

    while True:
        query = listen()
        
        if not query == None:
            if query == '':
                tts('Yes?')

            elif 'play' in query:
                playSong(query)
            
            elif 'the time' in query:
                tts(f'It\'s {getLocalTime()}')
            
            elif 'timer' in query:
                formattedTime = formatTime(query)
                tts(f'Setting a timer for {formatTime(query)[1]}')
                timer = threading.Thread(target=setTimer,args=[formattedTime])
                timer.start()

            elif 'weather' in query:
                tts('Showing the weather')
                webbrowser.open_new_tab('https://wttr.in/')

            elif 'what is' in query or "what's" in query:
                nums = 0
                try:
                    if 'what is' in query:
                        nums = query.split('what is ')[1]
                    else:
                        nums = query.split("what's ")[1]

                    numeval = nums.replace('x','*').replace('divided by','/').replace('percent','%')
                    numtext = nums.replace('x','times').replace('/','divided by').replace('%','percent')
                    
                    tts(f'{numtext} is {eval(numeval)}')
                    
                except:
                    googleSearch(query)
            else:
                googleSearch(query)

if __name__ == '__main__':
    while True:
        main()
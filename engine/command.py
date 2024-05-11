import pyttsx3
import speech_recognition as sr
import datetime
import eel
import os
import time




engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',190)


#This is a speak Fun() where Alita is able to speak'''
def speak(audio):

    engine.say(audio)
    eel.DisplayMessage(audio)
    eel.receiverText(audio)
    #print(audio)
    engine.runAndWait()
    
@eel.expose   
def takecommand():
    global query
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("\rListening...")
        eel.DisplayMessage('\rListening...')
        r.pause_threshold = 0.5
        audio = r.listen(source,10,6)

    try:
        print("\rRecognizing...")
        eel.DisplayMessage('\rRecognizing...')
        query = r.recognize_google(audio,language='en-in')
        eel.DisplayMessage(query)
        #time.sleep(2)
        #speak(query)
        #eel.ShowHood()

    except Exception as e:
        speak("Say that again please...")
        print("Say that again please...")
        takecommand()
        return

    return query.lower()

@eel.expose
def wish():
    hour=int(datetime.datetime.now().hour)

    if(hour>=0 and hour<=12):
        speak("Good Morning Master")
    elif(hour>=12 and hour<18):
        speak("Good Afternoon Master")
    else:
        speak("Good Evening Master")

    speak("Im Alita...Your Personal AI Assistant...Please tell me How can I help you")

#if __name__ == "__main__":

#takecommand()
#speak("Hi....Im Alita....Your Personal AI Assistant...How can I help you")
# wish()
# query=takecommand()
 #speak(query)

@eel.expose
def allCommand(message=1):
    
    if message == 1:
       query=takecommand()
       print(query)
       eel.senderText(query)
        
    else:
        query = message
        print(query)
        eel.senderText(query)
        query=query.lower()

    #print(query)
    try:
        from engine.features import switcher
        if query in switcher:
            func = switcher.get(query, lambda: speak("Invalid command"))
            func()
        else:
            from engine.features import conversation_handler
            #print(query)
            conversation_handler(query)

    except:  
        
        print("Error")
    
        
    eel.ShowHood()
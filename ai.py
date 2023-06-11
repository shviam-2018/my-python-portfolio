import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
#defining all veribal 
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
#defining audio and wishme 
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Good morning!")
        speak("Good morning!")
    elif hour>=12 and hour<18:
        print("Good afternoon")
        speak("Good afternoon!")
    else:
        print("Good evening!")
        speak("Good evening!")
        
    print("I am Campa sir. Please tell me how can I assist you today.")  
    speak("I am Campa sir. Please tell me how can I assist you today.")
    
#wishme() # call the wishme() function
    
def takecommand():
# it takes microphone input and ruterns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
    try: 
        print("recognizing...")
        query = r.recognize_google(audio, language="en-us")
        print(f"userside {query}\n")
        
    except Exception as e:
        print("say that agein please...")
        return "None"
    return query    

if __name__=="__main__":
    wishme()
    while True:
        query = takecommand().lower()
        
    #logich og exucuting task besced on query
        if "wikipedia" in query:
            speak("serching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikepedia")
            print(results)
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("youtube.com")
            
        elif "open google" in query:
            webbrowser.open("google.com")
            
        elif "open email" in query:
            webbrowser.open("mail.google.com")
            
        elif "search" in query:
            webbrowser.open("https://www.google.com/search?q=" + query)
            
        elif "open chat gpt" in query:
            webbrowser.open("https://chat.openai.com/chat")
        elif"study time" in query:
            print("coding time! or 10th prep")
            speak("coding time! or 10th prep")
            if query =="coding":
                open("https://vscode.dev/")
            elif "10th prep" in query:
                open("file:///C:/Users/sikok/OneDrive/Desktop/Lesson-00.pmd.pdf")
        
        
        else:
            print("i cant anser you i am sorry")
            speak("i cant anser you i am sorry")
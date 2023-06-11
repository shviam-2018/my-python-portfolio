import pyttsx3
while True:
    user_input = input("what do you what me to read? ")

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice",voices[0].id)
    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    print(user_input)
    speak(user_input)
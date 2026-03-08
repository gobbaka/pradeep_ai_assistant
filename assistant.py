import ollama
import speech_recognition as sr
import pyttsx3

# Speech recognizer
recognizer = sr.Recognizer()

# Text to speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust microphone noise
        recognizer.adjust_for_ambient_noise(source, duration=1)

        # Listen only for 3 seconds (faster)
        audio = recognizer.listen(source, phrase_time_limit=3)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text

    except:
        print("Could not understand")
        return None


def ask_ai(question):

    response = ollama.chat(
        model="tinyllama",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Give short and clear answers."},
            {"role": "user", "content": question}
        ]
    )

    answer = response["message"]["content"]
    return answer


# Main assistant loop
while True:

    user_text = listen()

    if user_text:
        answer = ask_ai(user_text)
        speak(answer)
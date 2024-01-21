from gtts import gTTS
import pygame
import os
import speech_recognition as sr
from llama_cpp import Llama
import time
import g4f
import v3

from g4f.Provider import (
    AItianhu,
    Aichat,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    OpenaiChat,
    Vercel,
    You,
    Yqcloud,
)

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.5f} seconds to execute.")
        return result
    return wrapper

# GLOBAL VARIABLES
my_model_path = "./model/zephyr-7b-beta.Q4_0.gguf"
CONTEXT_SIZE = 512
mymixer=pygame.mixer
mymixer.init()
flipper=True
# LOAD THE MODEL
zephyr_model = Llama(model_path=my_model_path, n_ctx=CONTEXT_SIZE)


@timing_decorator
def generate_text_from_prompt(
    user_prompt,
    max_tokens=200,
    temperature=0.3,
    top_p=0.1,
    echo=True,
    stop=["Question", "\n"]
):
    # Define the parameters
    model_output = zephyr_model(
        user_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        echo=echo,
        stop=stop,
    )

    final_result = model_output["choices"][0]["text"].strip().split("Answer: ")[1].strip()
    return final_result

@timing_decorator
def text_to_speech(text,flipper,language='en'):
    if flipper==True:
        filename="output.mp3"
    else: 
        filename="output2.mp3"
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(filename)

    # Load the generated audio file
    mymixer.music.load(filename)

    # Play the audio
    mymixer.music.play()

    # Wait for the audio to finish playing
    while mymixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Stop and close the audio resources
    mymixer.music.stop()
    #mymixer.quit()

    # Delete the generated audio file
    #os.remove("output.mp3")

@timing_decorator
def whatsup(text, language='en'):
    print("whatsup")

    
    mymixer.music.load("hi.mp3")
    mymixer.music.play()

    # Wait for the audio to finish playing
    while mymixer.music.get_busy():
        pygame.time.Clock().tick(10)

    mymixer.music.stop()
    #mymixer.quit()

@timing_decorator
def bye():
    print("goodbye")
    filename="bye.mp3"
    #tts = gTTS(text="Goodbye", lang="en", slow=False)
    #tts.save(filename)

    mymixer.music.load(filename)
    mymixer.music.play()

    # Wait for the audio to finish playing
    while mymixer.music.get_busy():
        pygame.time.Clock().tick(10)

    mymixer.music.stop()
    #mymixer.quit()

@timing_decorator
def record_and_transcribe():
    recognizer = sr.Recognizer()
    firsttime=0
    flipper=True

    with sr.Microphone() as source:
        print("Say 'Hey Bones' to start recording...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
        

        try:
            trigger_phrase = recognizer.recognize_google(audio_data).lower()
            if "goodbye" in trigger_phrase.lower() or "bye" in trigger_phrase.lower(): 
                bye()
                mymixer.quit()
                quit()
            if "bones" in trigger_phrase:

                while True:
                    print("Recording... Say your question.")
                    firsttime+=1
                    if firsttime==1:
                        whatsup("whats up?")
                    audio_data = recognizer.listen(source)
                    question = recognizer.recognize_google(audio_data)
                    print(f"You said: {question}")

                    # Exit the loop if the user says "stop" or similar
                    if "stop" in question.lower():
                        break

                    
                    

                    ## MAIN1 ##
                    # my_prompt = f"Question: {question}? Answer:"
                    # res = generate_text_from_prompt(my_prompt)
                    # print(res)
                    
                    ## MAIN2 ##
                    sent=''
                    response = g4f.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": question}],
                        stream=True,
                    )

                    #print(response)

                    for message in response:
                        if "[1" in str(message):break
                        if "https" in str(message) and "####" not in str(message):
                            print(message, flush=True, end='')
                            continue
                        sent+=str(message)
                        if "." in sent:
                            print(sent, flush=True, end='')
                            try:
                                text_to_speech(sent,flipper)
                                flipper=not flipper
                                sent=''
                            except:pass
                        else:
                            continue
                        #v3.run(message)

                    print(" ")

                    #text_to_speech(response,flipper)

                    #flipper=not flipper
                ## ---- ##
            else:
                print("Did not recognize 'Hey Bones'. Try again.")

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    x=0
    while x<10:
        cont=record_and_transcribe()
        x+=1

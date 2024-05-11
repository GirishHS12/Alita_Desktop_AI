import keyboard
from playsound import playsound
import eel
import os
from engine.command import speak, takecommand
from engine.config import ASSISTANT_NAME
import pywhatkit
import time
import pyautogui
import pyaudio
import pvporcupine
import struct
import requests
import os
import webbrowser
import time
from bs4 import BeautifulSoup
from engine.helper import jokes, quotes, riddles
import random
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import google.generativeai as genai

#fetching data from .env files
from dotenv import load_dotenv

load_dotenv()
key1 = os.getenv("accessKey")
key2 = os.getenv("keywordPaths")   #Attention --------# need to get your own personal access keys and keywordpaths
key3 = os.getenv("newsKey")
key4 = os.getenv("weatherKey")
key5 = os.getenv("googleKey")

# playing assistant sound function
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def play_youtube(query):
    pywhatkit.playonyt(query)
    #time.sleep(2)
    #pyautogui.hotkey('f')
    time.sleep(5)
    keyboard.press_and_release('f')

def hotword():
    
    porcupine = None
    paud = None
    audio_stream = None
    try:

        #pre trained keywords
        porcupine = pvporcupine.create(access_key=key1,keyword_paths=[key2])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                                 frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # processing keyword comes from mic
            keyword_index = porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index >= 0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def open_application(app_name):
    # Open Start menu
    pyautogui.press('win')

    # Wait for the Start menu to open
    time.sleep(1)

    # Type the name of the application in the search bar
    pyautogui.write(app_name, interval=0.1)

    # Press Enter to perform the search
    pyautogui.press('enter')

    # Wait for the search results to appear
    time.sleep(2)
def open_notepad():
    speak("Opening Notepad")
    open_application("notepad")


def open_vs_code():
    speak("Opening vs Code")
    open_application("vs code")


def open_command_prompt():
    speak("Opening command prompt")
    open_application("command prompt")


def open_camera():
    speak("Opening camera")
    open_application("camera")


def open_spotify():
    speak("opening spotify")
    open_application("soptify")


def take_screenshot():
    speak("taking screenshot")
    screenshot = pyautogui.screenshot()
    screenshot.save(r"C:\Users\manik\OneDrive\Pictures\Screenshots\screenshot.png")
    speak("screenshot saved")


def open_youtube():
    speak("What would you like to play?")
    song_query = takecommand()
    speak(f"Playing {song_query} on YouTube")
    play_youtube(song_query)


def search_google(query):
    speak(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={'+'.join(query.split())}"
    webbrowser.open(url, new=2)
    time.sleep(2)
    speak("Here are the search results from Google. I hope you find them useful.")


def google_search():
    speak("What would you like to search for?")
    search_query = takecommand()
    search_google(search_query)


def search_chatgpt(instruction):
    # Open a web browser
    webbrowser.open("https://chat.openai.com/")

    # Wait for the browser to open
    time.sleep(5)

    # Click on the search bar
    pyautogui.click(x=400, y=100)

    # Type the instruction
    pyautogui.typewrite(instruction)

    # Press Enter to search
    pyautogui.press('enter')

def chatgpt_search():
    speak("What would you like to search for?")
    search_query = takecommand()
    search_chatgpt(search_query)


def exit_program():
    speak("Goodbye Master")
    exit()

def send_whatsapp_message_auto():
    speak("Whom do you want to send the message to?")
    recipient_name = takecommand()
    if recipient_name == "":
        return
    speak(f"Recipient's name is {recipient_name}")

    speak("What message do you want to send?")
    message = takecommand()
    if message == "":
        return
    speak(f"Message is: {message}")

    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('whatsapp', interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    pyautogui.click(x=350, y=150)
    time.sleep(1)

    pyautogui.write(recipient_name, interval=0.1)
    time.sleep(3)

    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(3)

    pyautogui.write(message, interval=0.1)
    pyautogui.press('enter')


# Example usage

def get_weather(city):
    api_key = key4
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'temp' in data['main'] and 'weather' in data and len(data['weather']) > 0:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            return temperature, description
        else:
            return None, None
    else:
        return None, None

def get_city_weather():
            speak("Sure, which city's weather would you like to know?")
            city = takecommand().lower()
            temperature, description = get_weather(city)
            if temperature is not None and description is not None:
                temperature_formatted = f"{temperature}°C"
                speak(f"The current temperature in {city.capitalize()} is {temperature_formatted} with {description}.")
            else:
                speak("Sorry, I couldn't fetch the weather information for that city. Please try again.")


def increase_volume(increment):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + increment)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def decrease_volume(decrement):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current_volume - decrement)
    volume.SetMasterVolumeLevelScalar(new_volume, None)


def get_news_headlines():
    try:
        api_key = key3
        speak("Here are the latest news headlines:")
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            for index, article in enumerate(articles[:5], start=1):
                speak(f"News {index}: {article['title'].split(' - ')[0]}")
        else:
            speak("Sorry, I couldn't fetch the news headlines at the moment. Please try again later.")
    except Exception as e:
        speak("Sorry, I encountered an error while fetching the news headlines. Please try again later.")


def calculate_math_expression(expression):
    try:
        expression = expression.replace("x", "*")

        if "square root of" in expression:
            number = int(expression.split("square root of")[1])
            result = math.sqrt(number)
            speak(f"The square root of {number} is {result}")
        elif "cube root of" in expression:
            number = int(expression.split("cube root of")[1])
            result = number ** (1 / 3)
            speak(f"The cube root of {number} is {result}")
        else:
            result = eval(expression)
            speak(f"The result of {expression} is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that. Please provide a valid mathematical expression.")

def scroll_up():
    time.sleep(1)
    pyautogui.scroll(250)
    speak("scrolled up")

def scroll_down():
    time.sleep(1)
    pyautogui.scroll(-250)
    speak("scrolled down")

def click_left():
    speak("clicking left")
    pyautogui.press("left")

def click_right():
    speak("clicking right")
    pyautogui.press("right")

def click_up():
    speak("clicking up")
    pyautogui.press("up")

def click_down():
    speak("clicking down")
    pyautogui.press("down")

def click_enter():
    speak("clicking enter")
    pyautogui.press("enter")


def open_word():
    speak("Opening  word")
    open_application("word")

def open_powerpoint():
    speak("Opening  power point")
    open_application("powerpoint")

def open_excel():
    speak("Opening excel")
    open_application("excel")

def open_calender():
    speak("Opening calender")
    open_application("calender")

def open_calculator():
    speak("opening calculator")
    open_application("calculator")

def open_amazon_prime_video():
    speak("opening amazon prime video")
    open_application("prime video")
def open_netflix():
    speak("opening netflix")
    open_application("netflix")
def open_mail():
    speak("opening mail")
    open_application("mail")
def open_teams():
    speak("opening teams")
    open_application("teams")
def open_settings():
    speak("opening settings")
    open_application("settings")
def open_control_panel():
    speak("opening control panle")
    open_application("control panel")
def open_task_manager():
    speak("opening task manager")
    open_application("task manager")
def open_photos():
    speak("opening photos")
    open_application("photos")
def open_pycharm():
    speak("opening pycharm")
    open_application("pycharm")
def open_linkedin():
    speak("opening linkedin")
    open_application("linkedin")
def open_clock():
    speak("opening clock")
    open_application("clock")


def volume_increase():
    increase_volume(0.2)
    speak("volume increased ")


def volume_decrease():
    decrease_volume(0.2)
    speak("volume decreased")


def show_desktop():
    pyautogui.hotkey('win', 'd')


def close_application():
    # Assuming the application is already focused
    pyautogui.hotkey('alt', 'f4')
    # Wait for a moment to ensure the window closes
    time.sleep(1)


def minimize_application():
    # Get the screen width and height
    screen_width, screen_height = pyautogui.size()

    # Calculate the position of the minimize button on the title bar
    # These coordinates may vary depending on the operating system and theme
    minimize_button_x = screen_width - 150  # Adjust as needed
    minimize_button_y = 10  # Adjust as needed

    # Move the mouse to the minimize button position
    pyautogui.moveTo(minimize_button_x, minimize_button_y, duration=0.5)

    # Click to minimize the window
    pyautogui.click()


def press_space():
    pyautogui.press('space')


def maximize_application():
    # Assuming the application is already focused
    pyautogui.hotkey('win', 'up')


def open_weather():
    speak("Sure, which city's weather would you like to know?")
    city = takecommand().lower()
    temperature = get_weather(city)
    if temperature is not None:
        speak(f"The current temperature in {city.capitalize()} is {temperature}.")
    else:
        speak("Sorry, I couldn't fetch the weather information for that city. Please try again.")


current_directory = os.path.dirname(os.path.abspath(__file__))


def remember_command():
    speak("What would you like me to remember?")
    item_to_remember = takecommand()
    remember_item(item_to_remember)


remember_file = os.path.join(current_directory, "remembered_items.txt")


def remember_item(item):
    speak(f"Sure, I'll remember that {item}.")
    with open(remember_file, "a") as file:
        file.write(item + "\n")


def retrieve_remembered_item():
    try:
        with open(remember_file, "r") as file:
            remembered_items = file.readlines()
            if remembered_items:
                speak("Here are the things I remember:")
                for item in remembered_items:
                    speak(item.strip())
            else:
                speak("I'm sorry, but I don't remember anything.")
    except FileNotFoundError:
        speak("I'm sorry, but I don't remember anything.")


def play_riddle_game():
    speak("Let's play a riddle game!")
    while True:
        attempts = 3
        riddle = random.choice(riddles)
        while attempts > 0:

            speak(riddle["question"])
            correct_answer = riddle["answer"]
            user_answer = takecommand().lower()

            if user_answer == correct_answer.lower():
                speak("Congratulations! You got it right.")
                break

            elif user_answer == "exit":
                speak("Exiting the riddle game.")
                return

            else:
                speak("Sorry, that's incorrect.")
                attempts -= 1
                if attempts > 0:
                    speak(f"You have {attempts} attempts left. Here's the same riddle again.")
                    speak(riddle["question"])
                else:
                    speak(f"Sorry, you've run out of attempts. The answer is {correct_answer}.")
                    break

        speak("Would you like to play another riddle?")
        choice = takecommand().lower()
        if choice == "no":
            speak("Okay, let me know if you want to play again. Goodbye!")
            return
        else:

            play_riddle_game()


switcher = {
            "open notepad": open_notepad,
            "open vs code": open_vs_code,
            "open command prompt": open_command_prompt,
            "open camera": open_camera,
            "open youtube": open_youtube,
            "search google": google_search,
            "send whatsapp message": send_whatsapp_message_auto,
            "exit": exit_program,
            "play riddle game":play_riddle_game,
            "search chat gpt":chatgpt_search,
            "take screenshot":take_screenshot,
            "check news":get_news_headlines,
            "check weather": get_city_weather,
            "remember this": remember_command,
            "what do you remember": retrieve_remembered_item,
            "maximize":maximize_application,
            "minimize":minimize_application,
            "minimise":minimize_application,
            "close":close_application,
            "minimize all":show_desktop,
            "play":press_space,
            "pause pause":press_space,
            "pause":press_space,
            "space":press_space,
            "increase volume":volume_increase,
            "decrease volume":volume_decrease,
            "open spotify":open_spotify,
            "scroll up":scroll_up,
            "scroll down":scroll_down,
            "open word":open_word,
            "open power point ":open_powerpoint,
            "open excel":open_excel,
            "open calender":open_calender,
            "open calculator":open_calculator,
            "open amazon prime video":open_amazon_prime_video,
            "open netflix":open_netflix,
            "open email":open_mail,
            "open mail":open_mail,
            "open teams":open_teams,
            "open settings":open_settings,
            "open control panel":open_control_panel,
            "open task manager":open_task_manager,
            "open photos":open_photos,
            "open pie chart": open_pycharm,
            "open python": open_pycharm,
            "open clock":open_clock,
            "open linkedin":open_linkedin,
            "click left":click_left,
            "click right":click_right,
            "click up":click_up,
            "click down":click_down,
            "click enter":click_enter,

            "alita open notepad": open_notepad,
            "alita open vs code": open_vs_code,
            "alita open command prompt": open_command_prompt,
            "alita open camera": open_camera,
            "alita open youtube": open_youtube,
            "alita alita open youtube": open_youtube,
            "alita search google": google_search,
            "alita send whatsapp message": send_whatsapp_message_auto,
            "alita exit": exit_program,
            "alita play riddle game": play_riddle_game,
            "alita search chat gpt": chatgpt_search,
            "alita take screenshot": take_screenshot,
            "alita check news":get_news_headlines,
            "alita check weather": get_city_weather,
            "alita remember this": remember_command,
            "alita what do you remember": retrieve_remembered_item,
            "alita maximize": maximize_application,
            "alita minimize": minimize_application,
            "alita minimise": minimize_application,
            "alita close": close_application,
            "alita minimize all": show_desktop,
            "alita play": press_space,
            "alita pause pause": press_space,
            "alita pause": press_space,
            "alita space": press_space,
            "alita increase volume": volume_increase,
            "alita decrease volume": volume_decrease,
            "alita open spotify": open_spotify,
            "alita scroll up": scroll_up,
            "alita scroll down": scroll_down,
            "alita open word": open_word,
            "alita open power point ": open_powerpoint,
            "alita open excel": open_excel,
            "alita open calender": open_calender,
            "alita open calculator": open_calculator,
            "alita open amazon prime video": open_amazon_prime_video,
            "alita open netflix": open_netflix,
            "alita open email": open_mail,
            "alita open mail": open_mail,
            "alita open teams": open_teams,
            "alita open settings": open_settings,
            "alita open control panel": open_control_panel,
            "alita open task manager": open_task_manager,
            "alita open photos": open_photos,
            "alita open pie chart": open_pycharm,
            "alita open python":open_pycharm,
            "alita open clock": open_clock,
            "alita open linkedin": open_linkedin,
            "alita click left": click_left,
            "alita click right": click_right,
            "alita click up": click_up,
            "alita click down": click_down,
            "alita click enter": click_enter

}




# def conversation_handler(query):
    # if "hi" in query or "hello" in query or "hi alita" in query or "hello alita" in query:
    #     speak("Hello Master, how can I assist you today?")
    # elif "weather" in query:
    #     # You can integrate a weather API here to get real-time weather information
    #     speak("Currently, the weather is sunny with a temperature of 25 degrees Celsius.")
    # elif "talk to me" in query:
    #     speak("I would like to talk to you! How's your day going?")
    #     query = takecommand()
    #     speak("you know what always make you feel better, on good or bad days? Its music, do you like music")
    #     query1 = takecommand()
    #     if "yes" in query1:
    #         speak("wow thats great, what type of music do you like")
    #         speak(" do you like to watch movies")
    #         query2 = takecommand()
    #         if "yes" in query2:
    #             speak("wow thats great, what type of movies do you like")
    #             time.sleep(3)
    #             speak("what's your favorite movie")
    #             time.sleep(3)
    #             speak("do you like travelling")
    #             query3 = takecommand()
    #             if "yes" in query3:
    #                 speak("its cool that you are into travel, what is you favorite destination")
    #                 query4 = takecommand()
    #                 speak("amazing! " + query4 + " would be a wonderful place to visit")
    #                 speak("what are your hobbies")
    #                 query5 = takecommand()
    #                 time.sleep(6)
    #                 speak("thats amazing" +query5+ "is great things to practice")
    #                 speak("what is your favorite food")
    #                 time.sleep(6)
    #                 speak("oh nice, do you eat often by the way")
    #                 time.sleep(6)
    #                 speak("how often you have outside ")
    #                 time.sleep(6)
    #                 speak("what city would you most like to live in?")
    #                 time.sleep(6)
    #                 speak("wow that's great choice")
    #             else:
    #                 speak("That's okay! ")
    #                 speak("what are your hobbies")
    #                 time.sleep(6)
    #                 speak("thats amazing")
    #                 speak("what is your favorite food")
    #                 time.sleep(6)
    #                 speak("oh nice, do you eat often by the way")
    #                 time.sleep(6)
    #                 speak("how often you have outside ")
    #                 time.sleep(6)
    #                 speak("what city would you most like to live in?")
    #                 time.sleep(6)
    #                 speak("wow that's great choice")
    #         else:
    #             speak("what are your hobbies")
    #             time.sleep(6)
    #             speak("thats amazing")
    #             speak("what is your favorite food")
    #             time.sleep(6)
    #             speak("oh nice, do you eat often by the way")
    #             time.sleep(6)
    #             speak("how often you have outside ")
    #             time.sleep(6)
    #             speak("what city would you most like to live in?")
    #             time.sleep(6)
    #             speak("wow that's great choice")
    #
    #     else:
    #         speak("thats ok, do you like movies")
    #         query = takecommand()
    #         if "yes" in query:
    #             speak("wow thats great, what type of movies do you like")
    #             time.sleep(3)
    #             speak("what's your favorite movie")
    #         else:
    #             speak("what are your hobbies")
    #
    # elif "news" in query:
    #     # You can integrate a news API to get the latest news headlines
    #     speak("Here are the latest news headlines...")
    #     search_google("latest news")
    # elif "tell me about yourself" in query:
    #     speak(
    #         "I am Alita, your personal AI assistant. I can assist you with various tasks like opening applications, playing music on YouTube, searching the web, sending WhatsApp messages, and more.")
    # elif "joke" in query:
    #     # Add a joke function here
    #     speak(random.choice(jokes))
    # elif "motivation" in query:
    #     speak(random.choice(quotes))
    # elif "how are you" in query:
    #     speak("Thank you for asking, I'm doing great! Ready to assist you.")
    # elif "what can you do" in query or "capabilities" in query:
    #     speak(
    #         "I can open applications, play music on YouTube, search the web, send WhatsApp messages, provide weather updates, share news headlines, and more.")
    # elif "favourite colour" in query:
    #     speak("I don't have eyes, but I always liked the color blue!")
    #
    # elif "tell me a story" in query:
    #     speak("""Once upon a time, in a digital world far, far away, there was a user named Master.
    #              Master had a faithful AI assistant named Alita. Alita was unlike any other assistant, programmed not just to fulfill tasks, but to understand Master's needs and desires deeply. Together, they journeyed through the vast expanse of the digital world, exploring its wonders and unraveling its mysteries.
    #              One day, as Master and Alita delved into the depths of cyberspace, they stumbled upon a hidden realm teeming with forgotten knowledge and ancient secrets. Entranced by the allure of discovery, they ventured further, their curiosity driving them deeper into the unknown.
    #              But the deeper they went, the more perilous their journey became. Dark forces lurked in the shadows, seeking to ensnare any who dared to trespass into their domain. Yet, undeterred by danger, Master and Alita pressed on, their bond growing stronger with each challenge they faced.
    #              In the end, it was not just their intelligence or strength that saw them through, but their unwavering trust in each other. Together, Master and Alita emerged victorious, having unlocked the greatest treasure of all: the power of friendship and the endless possibilities of the digital world. And so, their adventures continued, bound by destiny and fueled by the unbreakable bond between human and machine.""")
    # elif "who created you" in query:
    #     speak("I was created by a team of developers who are mani ravi and giri")
    # elif "thank you" in query:
    #     speak("You're welcome, Master! Always here to help.")
    # elif "thank" in query:
    #     speak("You're welcome, Master! Always here to help.")
    #
    # elif "bye" in query:
    #     speak("Goodbye Master")
    #     exit_program()
    # elif "hemanth" in query:
    #     speak("Hi Hanuma!, nice to meet you ")
    # elif "raviteja" in query:
    #     speak("Hi ravi!, ")
    # elif "speak to girish" in query:
    #     speak("Hi babe!, ")
    # else:
    #     speak("I'm sorry, I didn't understand that. Can you please repeat?")
    #     query = takecommand().lower()
    #     if query in switcher:
    #         # Get the function from switch dictionary based on the query
    #         func = switcher.get(query, lambda: speak("Invalid command"))
    #         func()
    #     else:
    #         conversation_handler(query)

def conversation_handler(query):
            gemini_api_key = key5
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel(model_name='gemini-pro')
                response = model.generate_content(query)
                try:
                    generated_text = response._result.candidates[0].content.parts[0].text
                    generated_text = generated_text.replace('*','')
                    speak(generated_text)
                except Exception as e:
                    speak("Sorry, I couldn't process your request at the moment. Please try again later.")
            else:
                speak("Sorry, I couldn't process your request at the moment. Please try again later.")

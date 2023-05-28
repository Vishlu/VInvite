import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr


try:
    engine = pyttsx3.init()
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak: ")
        user_text = r.listen(source)
        print("Time over")

        speak = r.recognize_google(user_text)
        print(speak)
        engine.say(speak)
        engine.runAndWait()

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(
        "Could not request results from Google Speech Recognition service; {0}".format(e))

    Search_Input = speak

    url = "https://www.ask.com/web?q=" + Search_Input

    URL_response = requests.get(url)

    SearchAlgo_Soup = BeautifulSoup(URL_response.text, "html.parser")

    All_WebLinkContainer = []

    All_WebLink = SearchAlgo_Soup.find_all(
        'div', class_="PartialSearchResults-item")

    for web_link in All_WebLink:
        web_link_Heading = web_link.find("a").text
        web_link_FURL = web_link.find(
            "div", class_="PartialSearchResults-item-url").text
        web_link_FDesc = web_link.find(
            "p", class_="PartialSearchResults-item-abstract").text
        web_link_BURL = web_link.find(
            "a", class_="PartialSearchResults-item-title-link result-link").get("href")
        All_WebLinkContainer.append(
            (web_link_Heading, web_link_FURL, web_link_FDesc, web_link_BURL))

except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")


except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")

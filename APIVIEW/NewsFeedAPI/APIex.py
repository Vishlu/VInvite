import requests
from bs4 import BeautifulSoup

try:
    
    Search_Input = input("Enter Your Search: ")
    url = "https://www.ask.com/web?q=" + Search_Input
    URL_response = requests.get(url)
    soup = BeautifulSoup(URL_response.text, "html.parser")
    print(soup)

except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")

except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")
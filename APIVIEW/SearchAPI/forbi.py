import requests
from bs4 import BeautifulSoup

try:
    Search_Input = input("Enter Your Search: ")

    url = "https://www.ask.com/web?q=" + Search_Input

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    URL_response = requests.get(url, headers=headers)

    if URL_response.status_code == 200:
        SearchAlgo_Soup = BeautifulSoup(URL_response.text, "html.parser")

        All_WebLinkContainer = []

        All_WebLink = SearchAlgo_Soup.find_all('div', class_="PartialSearchResults-item")

        for web_link in All_WebLink:
            web_link_Heading = web_link.find("a").text
            web_link_FURL = web_link.find("div", class_="PartialSearchResults-item-url").text
            web_link_FDesc = web_link.find("p", class_="PartialSearchResults-item-abstract").text
            web_link_BURL = web_link.find("a", class_="PartialSearchResults-item-title-link result-link").get("href")
            All_WebLinkContainer.append((web_link_Heading, web_link_FURL, web_link_FDesc, web_link_BURL))
        print(All_WebLinkContainer)
    elif URL_response.status_code == 403:
        print("Error: 403 Forbidden. The website has denied access to the request. Please check if web scraping is allowed by the website's terms of service.")
    else:
        print(f"Error: {URL_response.status_code} {URL_response.reason}")
except requests.exceptions.ConnectionError as e:
    print("Error: Connection Error. Make sure you are connected to the Internet.")
except requests.Timeout as e:
    print("Error: Timeout Error")
except requests.RequestException as e:
    print("Error: General Error")
except KeyboardInterrupt:
    print("Someone closed the program")
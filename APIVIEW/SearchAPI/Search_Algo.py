# import requests
# from bs4 import BeautifulSoup

# Search_Input = input("Enter Your Search: ")

# url = "https://neeva.com/search"

# response = requests.get(url)
# print(response)
# SearchAlgo_Soup = BeautifulSoup(response.text, "html.parser")

# All_WebLinkContainer = []

# All_WebLink = SearchAlgo_Soup.find_all('li', attrs={"class" : "b_algo"})

# for web_link in All_WebLink:
# 	web_link_Heading =  web_link.find('a').text
# 	web_link_CLink = web_link.find('div', class_="b_attribution").text
# 	#web_link_Description = web_link.find('p',attrs={"class":"b_lineclamp2"})
# 	All_WebLinkContainer.append((web_link_Heading, web_link_CLink))
# print(All_WebLinkContainer)






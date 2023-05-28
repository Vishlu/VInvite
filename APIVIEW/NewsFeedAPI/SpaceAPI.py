import requests
from bs4 import BeautifulSoup

try: 
	Space_News_Url = "https://www.space.com/news" # space news
	Science_News_Url = "https://scitechdaily.com/news/science/"


	Space_News_Response = requests.get(Space_News_Url)
	Science_News_Response = requests.get(Science_News_Url)

	Space_News_Soup = BeautifulSoup(Space_News_Response.text, "html.parser")
	Science_News_Soup = BeautifulSoup(Science_News_Response.text, "html.parser")

	All_Space_News_PostContainer = []
	All_Science_News_PostContainer = []

	Space_News_PostContainer = Space_News_Soup.find_all('div', attrs={"data-page": "1"})
	Science_News_PostContainer = Science_News_Soup.find_all('div', class_="archive-list mh-section mh-group")

	for S_N in Space_News_PostContainer:
		SN_BURL = S_N.find('a').get('href')
		SN_Title = S_N.find('h3').text
		SN_Author = S_N.find('p', class_="byline").text
		SN_Time = S_N.find('time').text
		SN_Desc =S_N.find('p', class_="synopsis").text
		SN_Image = S_N.find('img').get('data-original-mos')
		All_Space_News_PostContainer.append((SN_BURL, SN_Title, SN_Author, SN_Time, SN_Desc, SN_Image))

	# only one data is comming
	for Sci_N in Science_News_PostContainer:
		SciN_BURL = Sci_N.find("a").get("href")
		SciN_Time = Sci_N.find('span', class_="entry-meta-date updated").text
		SciN_Title = Sci_N.find('h3').text
		SciN_Desc =Sci_N.find('div', class_="content-list-excerpt").text
		SciN_Image = Sci_N.find('img').get('src')
		All_Science_News_PostContainer.append((SciN_Time, SciN_Title, SciN_Desc, SciN_Image))

	print(All_Science_News_PostContainer)
except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")


except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")


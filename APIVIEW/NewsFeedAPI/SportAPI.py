import requests
from bs4 import BeautifulSoup

try:

	IndianExp_url = "https://indianexpress.com/section/sports/"
	TheHans_url = "https://www.thehansindia.com/sports"

	response = requests.get(IndianExp_url)
	Two_response = requests.get(TheHans_url)

	IndianExpress_Soup =  BeautifulSoup(response.text, "html.parser")
	TheHanIndia_Soup =  BeautifulSoup(Two_response.text, "html.parser")

	IndianExpress_Post = []
	TheHanIndia_Advert = []

	All_IndianExpress_PostContainer = IndianExpress_Soup.find_all('div', class_="articles")
	All_TheHanIndia_Advert = TheHanIndia_Soup.find_all('div', class_="col-md-4 ban-inner-content ban-inner-content-full")


	for Post_container in All_IndianExpress_PostContainer:
		Link = Post_container.find('a').get('href')
		Image_Link = Post_container.find('img').get("src")
		Image_Title = Post_container.find('h2', attrs={'class': 'title'}).text #class_="title"
		Image_Date = Post_container.find('div', attrs={'class': 'date'}).text # class_="date"
		Image_Desc = Post_container.find('p').text
		IndianExpress_Post.append((Link, Image_Link, Image_Title, Image_Date, Image_Desc))


	for Advert_container in All_TheHanIndia_Advert:
		One_Advert_IMG_Link = Advert_container.find('img').get('data-src')
		Two_Advert_Link = Advert_container.find('a').get('href')
		Three_Advert_IMG_Title = Advert_container.find('h2', class_="bdr-none").text
		TheHanIndia_Advert.append((One_Advert_IMG_Link, Two_Advert_Link, Three_Advert_IMG_Title))
	
	print("_______________")
	print(TheHanIndia_Advert)
	print(IndianExpress_Post)

except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")

except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")






import requests
from bs4 import BeautifulSoup

try:
	TimeOfIndia_url = "https://timesofindia.indiatimes.com/business/international-business"
	IndianExpress_url = "https://indianexpress.com/section/business/"
	Businesstoday_url = "https://www.businesstoday.in/"

	TimesOfIndia_response = requests.get(TimeOfIndia_url)
	IndianExpress_response = requests.get(IndianExpress_url)
	Businesstoday_response = requests.get(Businesstoday_url)

	TimesOfIndia_Soup = BeautifulSoup(TimesOfIndia_response.text, "html.parser")
	IndianExpress_Soup = BeautifulSoup(IndianExpress_response.text, "html.parser")
	Businesstoday_Soup = BeautifulSoup(Businesstoday_response.text, "html.parser")

	TimesOfIndia_And_Business_Standard_Banner_Container = []
	IndianExpress_Post_Container = []
	Businesstoday_TopNews_Container = []

	TimesOfIndia_Banner = TimesOfIndia_Soup.find_all('ul',class_="top-newslist clearfix")
	IndianExpress_Post = IndianExpress_Soup.find_all('div', class_="articles")
	Businesstoday_TopNews = Businesstoday_Soup.find_all('div', class_="bn_item")
	

	for Banner in TimesOfIndia_Banner:
		Banner_BURL = Banner.find('a').get('href')
		Banner_Image = Banner.find('img').get('src')
		Banner_Title = Banner.find('a').get('title')
		Banner_Time = Banner.find('span', class_="strlastupd").text
		TimesOfIndia_And_Business_Standard_Banner_Container.append((Banner_BURL, Banner_Image, Banner_Title, Banner_Time))

	for Post in IndianExpress_Post:
		Post_BURL = Post.find('a').get('href')
		PostImage_Link = Post.find('img').get("src")
		Post_Title = Post.find('h2', class_="title").text
		Post_Date = Post.find('div', class_="date").text
		Post_Desc = Post.find('p').text
		IndianExpress_Post_Container.append((Post_BURL, PostImage_Link, Post_Title, Post_Date, Post_Desc))

	for TopNews in Businesstoday_TopNews:
		TopNews_Cate = TopNews.find('div', class_="bn_item_cat").text
		TopNews_Desc =TopNews.find('h3').text
		TopNews_Image =TopNews.find('img').get('data-src')
		TopNews_BURL = TopNews.find('a').get('href')
		Businesstoday_TopNews_Container.append((TopNews_Cate, TopNews_Desc, TopNews_Image, TopNews_BURL))

	# print(Businesstoday_TopNews_Container)
	print(TimesOfIndia_And_Business_Standard_Banner_Container)
	print("_____________________________________________")
	print(IndianExpress_Post_Container)
	print("_____________________________________________")
	print(Businesstoday_TopNews_Container)
except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")


except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")
import requests
from bs4 import BeautifulSoup


try:
	Image_Input = input("Enter Your Image: ")

	Image_Url = "https://www.flickr.com/search/?text=" + Image_Input

	Image_response = requests.get(Image_Url)

	ImageAlgo_Soup = BeautifulSoup(Image_response.text, "html.parser")

	All_ImageLinkContainer = []

	All_ImageLink = ImageAlgo_Soup.find_all('div', class_="photo-list-photo-container")

	for ImageLink in All_ImageLink:
		Image_BURL = ImageLink.find("img").get('src')
		All_ImageLinkContainer.append(Image_BURL)
	print(All_ImageLinkContainer)
except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")


except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")
# print(All_ImageLinkContainer)
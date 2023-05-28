import requests
from bs4 import BeautifulSoup

try: 
	IndianExpress_U = "https://indianexpress.com/section/education/"
	thehansindia_U = "https://www.thehansindia.com/tags/Education"

	IndianExpress_R = requests.get(IndianExpress_U)
	thehansindia_R = requests.get(thehansindia_U)

	IndianExpress_S = BeautifulSoup(IndianExpress_R.text, "html.parser")
	thehansindia_S = BeautifulSoup(thehansindia_R.text, "html.parser")

	IndianExpress_All_PO = []
	thehansindia_All_B = []

	IndianExpress_P = IndianExpress_S.find_all('div', class_="articles")
	thehansindia_B = thehansindia_S.find_all('div', class_="col-md-4 ban-inner-content ban-inner-content-full")

	for IE_P in IndianExpress_P:
		P_BURL = IE_P.find('a').get('href')
		P_Image_L = IE_P.find('img').get("src")
		P_Title = IE_P.find('h2', class_="title").text
		P_Date = IE_P.find('div', class_="date").text
		P_Desc = IE_P.find('p').text
		IndianExpress_All_PO.append((P_BURL, P_Image_L, P_Title, P_Date, P_Desc))

	for Ban in thehansindia_B:
		B_BURL = Ban.find('a').get('href')
		B_Image = Ban.find("img").get("data-src")
		B_Title = Ban.find('h2').text
		thehansindia_All_B.append((B_BURL, B_Image, B_Title))

	print(thehansindia_All_B)

except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")


except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")
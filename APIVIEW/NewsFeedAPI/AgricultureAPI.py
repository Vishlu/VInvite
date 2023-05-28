import requests
from bs4 import BeautifulSoup

try:
	HandsIndia_U = "https://www.thehansindia.com/tags/Agriculture-Sector"
	TimesIndia_U ="https://timesofindia.indiatimes.com/topic/agriculture/news"

	HandsIndia_R = requests.get(HandsIndia_U)
	TimesIndia_R = requests.get(TimesIndia_U)

	HandsIndia_S = BeautifulSoup(HandsIndia_R.text, "html.parser")
	TimesIndia_S = BeautifulSoup(TimesIndia_R.text, "html.parser")

	HandsIndia_All_B = []
	TimesIndia_All_PO = []

	HandsIndia_B = HandsIndia_S.find_all('div', class_="col-md-4 ban-inner-content ban-inner-content-full")
	TimesIndia_P = TimesIndia_S.find_all('div', class_="Mc7GB")

	for B in HandsIndia_B:
		BH_BURL = B.find('a').get('href')
		BH_Image = B.find("img").get("data-src")
		BH_Title = B.find('h2').text
		HandsIndia_All_B.append((BH_BURL, BH_Image, BH_Title))


	for TI_P in TimesIndia_P:
		TI_P_BURL = TI_P.find('a').get('href')
		TI_P_Image_L = TI_P.find("img").get("src")
		TI_P_Title = TI_P.find('div', class_="EW1Mb _3v379").text
		TI_P_Date = TI_P.find('div', class_="hVLK8").text
		TI_P_Desc = TI_P.find('p').text
		TimesIndia_All_PO.append((TI_P_BURL, TI_P_Image_L, TI_P_Title, TI_P_Date, TI_P_Desc))
		
	print(HandsIndia_All_B)

except requests.exceptions.ConnectionError as e:
    print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

except requests.Timeout as e:
    print("OOPS!! Timeout Error")


except requests.RequestException as e:
    print("OOPS!! General Error")

except KeyboardInterrupt:
    print("Someone closed the program")
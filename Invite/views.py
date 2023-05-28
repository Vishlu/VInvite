import urllib.request as request
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import UserProfileModelForm
from .models import User_Profile
from django.contrib import messages
import speech_recognition as sr
from bs4 import BeautifulSoup
import pyttsx3
import requests
import time
import re
import threading
import lxml


@login_required(login_url='sign-in-btn')
def VoiceRecognition(request):
    try:

        st = time.time()
        engine = pyttsx3.init()
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak: ")
            user_text = r.listen(source)
            print("Time over")

            speak = r.recognize_google(user_text)
            print(speak)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say("Hey you Search for " + speak)
            engine.runAndWait()
            engine = None

            url = "https://www.ask.com/web?q=" + speak
            Image_Url = "https://www.flickr.com/search/?text=" + speak
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            URL_response = requests.get(url, headers=headers)
            Image_response = requests.get(Image_Url)

            if Image_response.status_code == 200:
                ImageAlgo_Soup = BeautifulSoup(
                    Image_response.text, "html.parser")

            if URL_response.status_code == 200:
                SearchAlgo_Soup = BeautifulSoup(
                    URL_response.text, "html.parser")

                All_WebLink = SearchAlgo_Soup.find_all(
                    'div', class_="PartialSearchResults-item")
                All_ImageLink = ImageAlgo_Soup.find_all(
                    'div', class_="photo-list-photo-container")

                All_WebLinkContainer = []
                All_ImageLinkContainer = []

                for web_link in All_WebLink:
                    web_link_Heading = web_link.find("a").text
                    web_link_FURL = web_link.find("div", class_="PartialSearchResults-item-url").text
                    web_link_FDesc = web_link.find("p", class_="PartialSearchResults-item-abstract").text
                    web_link_BURL = web_link.find("a", class_="PartialSearchResults-item-title-link result-link").get("href")
                    All_WebLinkContainer.append((web_link_Heading, web_link_FURL, web_link_FDesc, web_link_BURL))

                for ImageLink in All_ImageLink:
                    Image_BURL = ImageLink.find("img").get('src')
                    All_ImageLinkContainer.append(Image_BURL)

                NUM_All_WebLinkContainer = len(All_WebLinkContainer)
                NUM_All_ImageLinkContainer = len(All_ImageLinkContainer)
                et = time.time()
                execution_time = et - st
                final_execution_time = execution_time / 60
                return render(request, "Invite/InformationTab.html",
                              {'All_WebLinkContainer_Key': All_WebLinkContainer, 'Num_All_WebLinkContainer_Key': NUM_All_WebLinkContainer, 'All_ImageLinkContainer': All_ImageLinkContainer, 'NUM_All_ImageLinkContainer': NUM_All_ImageLinkContainer, 'final_execution_time': final_execution_time})

    except RuntimeError:
        return redirect('/aleneous-voice')
        # return HttpResponse("run loop already started")

    except sr.UnknownValueError:
        return redirect('/aleneous-voice')
        # return HttpResponse("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        return HttpResponse("Could not request results from Google Speech Recognition service; {0}".format(e))
    except requests.exceptions.ConnectionError as e:
        return HttpResponse("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")

    except requests.Timeout as e:
        return HttpResponse("OOPS!! Timeout Error")

    except requests.RequestException as e:
        return HttpResponse("OOPS!! General Error")

    except KeyboardInterrupt:
        return HttpResponse("Someone closed the program")


def Visitors_Home(request):
    if not request.user.is_authenticated:
        pass
    else:
        return redirect('/user-home')
    return render(request, "Invite/VisitorsHome.html")


def SignUp_Task(Reg_User, Reg_Email, Reg_Pass):
    R_AU = User.objects.create_user(Reg_User, Reg_Email, Reg_Pass)
    R_AU.save()


def Sign_Up(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            Reg_User = request.POST['Ruser-name']
            Reg_Firstn = request.POST['Rfirst-name']
            Reg_Lastn = request.POST['Rlast-name']
            Reg_Email = request.POST['Remail']
            Reg_Pass = request.POST['Rpassword']
            R_Repas = request.POST['Rre-password']

            if len(Reg_User) < 3 or Reg_User is None:
                messages.error(
                    request, "Aleneous Must be more than 3 Character.")
                return redirect('/sign-up')

            if not Reg_User.isalnum():
                messages.error(request, "Aleneous Must be Alpha Numeric!")
                return redirect('/sign-up')

            if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", Reg_Email):
                messages.error(
                    request, f"The Aleneous address {Reg_Email} is not valid")
                return redirect('/sign-up')

            if Reg_Pass != R_Repas:
                messages.error(request, "AccessKey does not Match!")
                return redirect('/sign-up')

            if len(Reg_Pass) < 5:
                messages.error(request, "AccessKey Must be More than 6 Keys")
                return redirect('/sign-up')

            t = threading.Thread(target=SignUp_Task, args=(
                Reg_User, Reg_Email, Reg_Pass))
            t.start()
            messages.success(request, "You're Generated Access Key")
            return redirect('/sign-in')
    else:
        return redirect('/sign-up')
    return render(request, "Invite/SignUp.html")


def SignIn_Task(request, alien_username, alien_password):
    alien_user = authenticate(username=alien_username, password=alien_password)
    if alien_user is not None:
        login(request, alien_user)
        return True
    else:
        return False


def Sign_In(request):
    # Clear messages framework between requests
    storage = messages.get_messages(request)
    for message in storage:
        pass

    if not request.user.is_authenticated:
        if request.method == 'POST':
            alien_username = request.POST['Luser-name']
            alien_password = request.POST['Luser-pass']
            # Call SignIn_Task function synchronously
            success = SignIn_Task(request, alien_username, alien_password)
            if success:
                messages.success(request, "You Accesssed Successfully.")
                return render(request, "Invite/UserProfile.html")
            else:
                messages.error(request, "Invalid AccessKey!")
                return redirect('/sign-in')

    else:
        messages.success(request, "You are already logged in.. User")
        return redirect('/user-home')

    return render(request, "Invite/SignIn.html")


def Sign_Out(request):
    logout(request)
    return redirect('/')


@login_required(login_url='sign-in-btn')
def User_Home(request):
    try:
        login_user = User_Profile.objects.get(user=request.user)
    except Exception as e:
        login_user = None
        print("Exception: ", e)
        return redirect("/addprofile-info")

    return render(request, "Invite/UserProfile.html", {'login_user': login_user})


def addUserProfile(request):
    user = request.user
    if request.method == 'POST':
        user_profileform = UserProfileModelForm(request.POST, request.FILES)
        if user_profileform.is_valid():
            img = user_profileform.cleaned_data['images']
            fn = user_profileform.cleaned_data['first_name']
            ln = user_profileform.cleaned_data['last_name']
            bi = user_profileform.cleaned_data['Bio']

            userprofile_DB = User_Profile(
                images=img, first_name=fn, last_name=ln, Bio=bi)
            add_profileData = user_profileform.save(commit=False)
            add_profileData.user = user
            user_profileform.save()
            return redirect('/user-home')
    else:
        user_profileform = UserProfileModelForm()
    return render(request, "Invite/addProfile.html", {'user_profileform': user_profileform})


@login_required(login_url='sign-in-btn')
def Meet(requests):
    return render(requests, "Invite/Meet.html")


@login_required(login_url='sign-in-btn')
def Sports_Feed(request):
    try:
        IndianExp_url = "https://indianexpress.com/section/sports/"
        TheHans_url = "https://www.thehansindia.com/sports"

        response = requests.get(IndianExp_url)
        Two_response = requests.get(TheHans_url)

        IndianExpress_Soup = BeautifulSoup(response.text, "lxml")
        TheHanIndia_Soup = BeautifulSoup(Two_response.text, "lxml")

        IndianExpress_Post = []
        TheHanIndia_Advert = []

        All_IndianExpress_PostContainer = IndianExpress_Soup.find_all(
            'div', class_="articles")
        All_TheHanIndia_Advert = TheHanIndia_Soup.find_all(
            'div', class_="col-md-4 ban-inner-content ban-inner-content-full")

        for Post_container in All_IndianExpress_PostContainer:
            Link = Post_container.find('a').get('href')
            Image_Link = Post_container.find('img').get("src")
            Image_Title = Post_container.find(
                'h2', attrs={'class': 'title'}).text  # class_="title"
            Image_Date = Post_container.find(
                'div', attrs={'class': 'date'}).text  # class_="date"
            Image_Desc = Post_container.find('p').text
            IndianExpress_Post.append(
                (Link, Image_Link, Image_Title, Image_Date, Image_Desc))

        for Advert_container in All_TheHanIndia_Advert:
            One_Advert_IMG_Link = Advert_container.find('img').get('data-src')
            Two_Advert_Link = Advert_container.find('a').get('href')
            Three_Advert_IMG_Title = Advert_container.find(
                'h2', class_="bdr-none").text
            TheHanIndia_Advert.append(
                (One_Advert_IMG_Link, Two_Advert_Link, Three_Advert_IMG_Title))

    except requests.exceptions.ConnectionError as e:
        HttpResponse(
            "OOPS!! Connection Error. Make sure you are connected to Internet.\n")

    except requests.Timeout as e:
        HttpResponse("OOPS!! Timeout Error")

    except requests.RequestException as e:
        HttpResponse("OOPS!! General Error")

    except KeyboardInterrupt:
        HttpResponse("Someone closed the program")
    # 'TheHanIndia_Advert': TheHanIndia_Advert,
    return render(request, "Invite/SportsFeed.html", {'IndianExpress_Post': IndianExpress_Post, 'TheHanIndia_Advert': TheHanIndia_Advert})


@login_required(login_url='sign-in-btn')
def Bsuiness_Feed(request):
    try:
        TimesOfIndia_And_Business_Standard_Banner_Container = []
        IndianExpress_Post_Container = []
        Businesstoday_TopNews_Container = []

        TimeOfIndia_url = "https://timesofindia.indiatimes.com/business/international-business/"
        IndianExpress_url = "https://indianexpress.com/section/business/"
        Businesstoday_url = "https://www.businesstoday.in/"

        TimesOfIndia_response = requests.get(TimeOfIndia_url)
        IndianExpress_response = requests.get(IndianExpress_url)
        Businesstoday_response = requests.get(Businesstoday_url)

        if TimesOfIndia_response.status_code == 200:
            TimesOfIndia_Soup = BeautifulSoup(
                TimesOfIndia_response.text, "lxml")
        if IndianExpress_response.status_code == 200:
            IndianExpress_Soup = BeautifulSoup(
                IndianExpress_response.text, "lxml")
        if Businesstoday_response.status_code == 200:
            Businesstoday_Soup = BeautifulSoup(
                Businesstoday_response.text, "lxml")

            TimesOfIndia_Banner = TimesOfIndia_Soup.find_all(
                'ul', class_="top-newslist clearfix")
            IndianExpress_Post = IndianExpress_Soup.find_all(
                'div', class_="articles")
            Businesstoday_TopNews = Businesstoday_Soup.find_all(
                'div', class_="bn_item")

            for Banner in TimesOfIndia_Banner:
                Banner_BURL = Banner.find('a').get('href')
                Banner_Image = Banner.find('img').get('src')
                Banner_Title = Banner.find('a').get('title')
                Banner_Time = Banner.find('span', class_="strlastupd").text
                TimesOfIndia_And_Business_Standard_Banner_Container.append(
                    (Banner_BURL, Banner_Image, Banner_Title, Banner_Time))

            for Post in IndianExpress_Post:
                Post_BURL = Post.find('a').get('href')
                PostImage_Link = Post.find('img').get("src")
                Post_Title = Post.find('h2', class_="title").text
                Post_Date = Post.find('div', class_="date").text
                Post_Desc = Post.find('p').text
                IndianExpress_Post_Container.append(
                    (Post_BURL, PostImage_Link, Post_Title, Post_Date, Post_Desc))

            for TopNews in Businesstoday_TopNews:
                TopNews_Cate = TopNews.find('div', class_="bn_item_cat").text
                TopNews_Desc = TopNews.find('h3').text
                TopNews_Image = TopNews.find('img').get('data-src')
                TopNews_BURL = TopNews.find('a').get('href')
                Businesstoday_TopNews_Container.append(
                    (TopNews_Cate, TopNews_Desc, TopNews_Image, TopNews_BURL))

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("<center><br><br>OOPS!! Connection Error. Make sure you are connected to Internet.</center>")

    except requests.Timeout as e:
        return HttpResponse("OOPS!! Timeout Error")

    except requests.RequestException as e:
        return HttpResponse("OOPS!! General Error")

    except KeyboardInterrupt:
        return HttpResponse("Someone closed the program")

    return render(request, "Invite/BusinessFeed.html",
                  {'Business_Banner': TimesOfIndia_And_Business_Standard_Banner_Container, 'IndianExpress_Post_Container': IndianExpress_Post_Container, 'Businesstoday_TopNews_Container': Businesstoday_TopNews_Container})


@login_required(login_url='sign-in-btn')
def Space_Feed(request):

    try:
        All_Space_News_PostContainer = []
        All_Science_News_PostContainer = []

        Space_News_Url = "https://www.space.com/news"  # space news
        Science_News_Url = "https://scitechdaily.com/news/science/"

        Space_News_Response = requests.get(Space_News_Url)
        Science_News_Response = requests.get(Science_News_Url)

        if Space_News_Response.status_code == 200:
            Space_News_Soup = BeautifulSoup(
                Space_News_Response.text, "lxml")
        if Science_News_Response.status_code == 200:
            Science_News_Soup = BeautifulSoup(
                Science_News_Response.text, "lxml")

            Space_News_PostContainer = Space_News_Soup.find_all(
                'div', attrs={"data-page": "1"})
            Science_News_PostContainer = Science_News_Soup.find_all(
                'div', class_="archive-list mh-section mh-group")

        for S_N in Space_News_PostContainer:
            SN_BURL = S_N.find('a').get('href')
            SN_Title = S_N.find('h3').text
            SN_Author = S_N.find('p', class_="byline").text
            SN_Time = S_N.find('time').text
            SN_Desc = S_N.find('p', class_="synopsis").text
            SN_Image = S_N.find('img').get('data-original-mos')
            All_Space_News_PostContainer.append(
                (SN_BURL, SN_Title, SN_Author, SN_Time, SN_Desc, SN_Image))

        # only one data is comming
        for Sci_N in Science_News_PostContainer:
            SciN_BURL = Sci_N.find("a").get("href")
            SciN_Time = Sci_N.find(
                'span', class_="entry-meta-date updated").text
            SciN_Title = Sci_N.find('h3').text
            SciN_Desc = Sci_N.find('div', class_="content-list-excerpt").text
            SciN_Image = Sci_N.find('img').get('src')
            All_Science_News_PostContainer.append(
                (SciN_BURL, SciN_Time, SciN_Title, SciN_Desc, SciN_Image))

    except requests.exceptions.ConnectionError as e:
        return HttpResponse(
            "OOPS!! Connection Error. Make sure you are connected to Internet.\n")

    except requests.Timeout as e:
        return HttpResponse("OOPS!! Timeout Error")

    except requests.RequestException as e:
        return HttpResponse("OOPS!! General Error")

    except KeyboardInterrupt:
        return HttpResponse("Someone closed the program")

    return render(request, "Invite/SpaceFeed.html", {'All_Space_News_PostContainer': All_Space_News_PostContainer, 'All_Science_News_PostContainer': All_Science_News_PostContainer})


@login_required(login_url='sign-in-btn')
def Education_Feed(request):

    try:
        IndianExpress_All_PO = []
        thehansindia_All_B = []

        IndianExpress_U = "https://indianexpress.com/section/education/"
        thehansindia_U = "https://www.thehansindia.com/tags/Education"

        IndianExpress_R = requests.get(IndianExpress_U)
        thehansindia_R = requests.get(thehansindia_U)

        if IndianExpress_R.status_code == 200:
            IndianExpress_S = BeautifulSoup(
                IndianExpress_R.text, "lxml")

        if thehansindia_R.status_code == 200:
            thehansindia_S = BeautifulSoup(thehansindia_R.text, "lxml")

            IndianExpress_P = IndianExpress_S.find_all(
                'div', class_="articles")
            thehansindia_B = thehansindia_S.find_all(
                'div', class_="col-md-4 ban-inner-content ban-inner-content-full")

        for IE_P in IndianExpress_P:
            P_BURL = IE_P.find('a').get('href')
            P_Image_L = IE_P.find('img').get("src")
            P_Title = IE_P.find('h2', class_="title").text
            P_Date = IE_P.find('div', class_="date").text
            P_Desc = IE_P.find('p').text
            IndianExpress_All_PO.append(
                (P_BURL, P_Image_L, P_Title, P_Date, P_Desc))

        for Ban in thehansindia_B:
            B_BURL = Ban.find('a').get('href')
            B_Image = Ban.find("img").get("data-src")
            B_Title = Ban.find('h2').text
            thehansindia_All_B.append((B_BURL, B_Image, B_Title))

    except requests.exceptions.ConnectionError as e:
        return HttpResponse(
            "OOPS!! Connection Error. Make sure you are connected to Internet. \n")

    except requests.Timeout as e:
        return HttpResponse("OOPS!! Timeout Error")

    except requests.RequestException as e:
        return HttpResponse("OOPS!! General Error")

    except KeyboardInterrupt:
        return HttpResponse("Someone closed the program")

    return render(request, "Invite/EducationFeed.html", {'IndianExpress_All_PO': IndianExpress_All_PO, 'thehansindia_All_B': thehansindia_All_B})


@login_required(login_url='sign-in-btn')
def Agriculture_Feed(request):

    try:
        HandsIndia_All_B = []
        TimesIndia_All_PO = []

        HandsIndia_U = "https://www.thehansindia.com/tags/Agriculture-Sector"
        TimesIndia_U = "https://timesofindia.indiatimes.com/topic/agriculture/news"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        HandsIndia_R = requests.get(HandsIndia_U, headers=headers)
        TimesIndia_R = requests.get(TimesIndia_U, headers=headers)
        if HandsIndia_R.status_code == 200:
            HandsIndia_S = BeautifulSoup(HandsIndia_R.text, "lxml")

        if TimesIndia_R.status_code == 200:
            TimesIndia_S = BeautifulSoup(TimesIndia_R.text, "lxml")

            HandsIndia_B = HandsIndia_S.find_all(
                'div', class_="col-md-4 ban-inner-content ban-inner-content-full")
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
        print(TimesIndia_All_PO)
    except requests.exceptions.ConnectionError as e:
        return HttpResponse(
            "OOPS!! Connection Error. Make sure you are connected to Internet. \n")

    except requests.Timeout as e:
        return HttpResponse("OOPS!! Timeout Error")

    except requests.RequestException as e:
        return HttpResponse("OOPS!! General Error")

    except KeyboardInterrupt:
        return HttpResponse("Someone closed the program")
    return render(request, "Invite/AgricultureFeed.html", {'HandsIndia_All_B': HandsIndia_All_B, 'TimesIndia_All_PO': TimesIndia_All_PO})


@login_required(login_url='sign-in-btn')
def UserQuery_Information(request):
    try:
        st = time.time()
        if request.method == "POST":
            Search_Input = request.POST.get('dynamic-input')
            url = "https://www.ask.com/web?q=" + Search_Input
            Image_Url = "https://www.flickr.com/search/?text=" + Search_Input
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            URL_response = requests.get(url, headers=headers)
            Image_response = requests.get(Image_Url)

            if Image_response.status_code == 200:
                ImageAlgo_Soup = BeautifulSoup(
                    Image_response.text, "lxml")

            if URL_response.status_code == 200:
                SearchAlgo_Soup = BeautifulSoup(URL_response.text, "lxml")

                All_WebLink = SearchAlgo_Soup.find_all('div', class_="PartialSearchResults-item")
                All_ImageLink = ImageAlgo_Soup.find_all('div', class_="photo-list-photo-container")

                All_WebLinkContainer = []
                All_ImageLinkContainer = []

                for web_link in All_WebLink:
                    web_link_Heading = web_link.find("a").text
                    web_link_FURL = web_link.find("div", class_="PartialSearchResults-item-url").text
                    web_link_FDesc = web_link.find("p", class_="PartialSearchResults-item-abstract").text
                    web_link_BURL = web_link.find("a", class_="PartialSearchResults-item-title-link result-link").get("href")
                    All_WebLinkContainer.append((web_link_Heading, web_link_FURL, web_link_FDesc, web_link_BURL))

                for ImageLink in All_ImageLink:
                    Image_BURL = ImageLink.find("img").get('src')
                    All_ImageLinkContainer.append(Image_BURL)

                NUM_All_WebLinkContainer = len(All_WebLinkContainer)
                NUM_All_ImageLinkContainer = len(All_ImageLinkContainer)
                et = time.time()
                execution_time = et - st
                final_execution_time = (execution_time / 60)
                # print(All_ImageLinkContainer)
                print(All_WebLinkContainer)
                return render(request, "Invite/InformationTab.html",
                              {'All_WebLinkContainer_Key': All_WebLinkContainer, 'Num_All_WebLinkContainer_Key': NUM_All_WebLinkContainer, 'All_ImageLinkContainer': All_ImageLinkContainer, 'NUM_All_ImageLinkContainer': NUM_All_ImageLinkContainer, 'final_execution_time': final_execution_time})

    except requests.exceptions.ConnectionError as e:
        return HttpResponse("OOPS!! Connection Error. Make sure you are connected to Internet.\n")

    except requests.Timeout as e:
        return HttpResponse("OOPS!! Timeout Error")

    except requests.RequestException as e:
        return HttpResponse("OOPS!! General Error")

    except KeyboardInterrupt:
        return HttpResponse("Someone closed the program")
    return render(request, "Invite/InformationTab.html")


def Privacy_Policy(request):
    return render(request, "Invite/PrivacyPolicy.html")


def Terms_Condition(request):
    return render(request, "Invite/TermsCondition.html")


def About_Us(request):
    return render(request, "Invite/AboutUs.html")


def Community(request):
    return render(request, "Invite/Community.html")

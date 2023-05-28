from django.urls import path
from Invite import views
import random
import string

n = 6
code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
maincode = str(code)

urlpatterns = [
    path('', views.Visitors_Home, name="visitors-home-btn"),
    path('sign-up/', views.Sign_Up, name="sign-up-btn"),
    path('sign-in/', views.Sign_In, name="sign-in-btn"),
    path('sign-out/', views.Sign_Out, name="sign-out-btn"),
    path('user-home/', views.User_Home, name="user-home-btn"),
    path('addprofile-info/', views.addUserProfile, name='addprofile-info-btn'),
    path('aleneous-meet/', views.Meet, name='meet-btn'),
    path('aleneous-voice/', views.VoiceRecognition, name='voice-btn'),
    
    path('user-Query/', views.UserQuery_Information, name="query-info"),
    path('sports-feed/', views.Sports_Feed, name="sport-btn"),
    path('business-feed/', views.Bsuiness_Feed, name="business-btn"),
    path('space-feed/', views.Space_Feed, name="space-btn"),
    path('education-feed/', views.Education_Feed, name="education-btn"),
    path('agriculture-feed/', views.Agriculture_Feed, name="agriculture-btn"),
    
    path('privacy-policy/', views.Privacy_Policy, name='pri-pol-btn'),
    path('terms-condition/', views.Terms_Condition, name='tem-con-btn'),
    path('about-us/', views.About_Us, name='about-us-btn'),
    path('community/', views.Community, name='commun-btn'),
]

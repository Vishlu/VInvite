from django.contrib import admin
from .models import User_Profile, User
# Register your models here.

@admin.register(User_Profile)
class UserProfile_Admin(admin.ModelAdmin):
    list_display = ['user', 'Bio']

@admin.register(User)
class UserIPAddress_Admin(admin.ModelAdmin):
    list_display=['user']

from django import forms
from .models import User_Profile

class UserProfileModelForm(forms.ModelForm):
    images = forms.ImageField()
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'f-name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'l-name'}))
    Bio = forms.CharField(error_messages={'required': 'Write something about you.'}, widget=forms.Textarea(attrs={'class': 'bio-name' , 'max_length': 150}))
    class Meta:
        model = User_Profile
        fields = ['images', 'first_name', 'last_name', 'Bio']



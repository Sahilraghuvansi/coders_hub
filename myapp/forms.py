from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import *


class RegisterForm(UserCreationForm):
    # first_name=forms.CharField(max_length=200)
    # last_name=forms.CharField(max_length=200)
    # email = forms.EmailField()
   

    class Meta:
        model =CustomUser
        fields = ["first_name","last_name","username","email","password1","password2","user_type","image"]


        
class loginForm(forms.Form):
    username=forms.CharField(max_length=200)
    password=forms.CharField(max_length=200)



class projectForm(forms.ModelForm):
    title=forms.CharField(max_length=200)
    descreption=forms.CharField(max_length=200)
    budget=forms.CharField(max_length=200)


    class Meta:
        model=project
        fields=["title","descreption","budget"]



class proposalForm(forms.ModelForm):
    coverlet=forms.CharField(max_length=200)
    amount=forms.CharField(max_length=200)
  
    class Meta:
        model=proposal
        fields=["coverlet","amount"]
        


class MessageForm(forms.ModelForm):
    # subject=forms.CharField(max_length=200)
    mesg=forms.CharField(max_length=200) 

    class Meta:
        model=Message
        fields=["mesg"]

class MessageForm2(forms.ModelForm):
    # subject=forms.CharField(max_length=200)
    mesg=forms.CharField(max_length=200) 

    class Meta:
        model=Message
        fields=["mesg"]


# class imagesform(forms.ModelForm):
#     class Meta:
#         model = images
#         fields = ['image']


class PicturesForm(forms.ModelForm):
    class Meta:
        model=Images
        fields=["files"]



class PhoneNumberVerificationForm(forms.ModelForm):
    phone_number = models.IntegerField(max_length=10)

    class Meta:
        model = Mobile
        fields = ['phone_number']

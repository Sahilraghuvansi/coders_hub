import os
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
# from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.

# model = project

ADMIN="1"
CLIENT="2"
FREELANCER="3"

class CustomUser(AbstractUser):
    USER_TYPES = (
        (CLIENT, '2'),
        (FREELANCER, '3'),
    )
    user_type =models.CharField(max_length=10,choices=USER_TYPES,default=1)
    image = models.ImageField(upload_to='images/',default=0)

    def __str__(self):
        return str(self.user_type)

class project(models.Model):
    title=models.CharField(max_length=100)
    descreption= models.CharField(max_length=200)
    budget=models.CharField(max_length=150)
    created_by= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    CreatedAt=models.DateTimeField(auto_now=True)


class proposal(models.Model):
    freelancer=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    project=models.ForeignKey(project,on_delete=models.CASCADE)
    coverlet= models.CharField(max_length=200)
    amount=models.CharField(max_length=150)
    createdAt=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=150)
    

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    # subject = models.CharField(max_length=200)
    mesg = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # sender_type= models.CharField(max_length=200)


# class images(models.Model):
#     profile_img=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images/',default=0)
   
    
# def create_user_folder(sender, instance, created, **kwargs):
#     if created:
#         # Create a folder for the user using their username as the folder name
#         folder_path = os.path.join('media/folder/', instance.username)

#         # Create the folder
#         os.makedirs(folder_path, exist_ok=True)



class Images(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    files = models.ImageField(upload_to='')




class Profile(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Mobile(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    is_phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)


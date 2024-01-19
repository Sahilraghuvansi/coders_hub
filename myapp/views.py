import os
import uuid
# from tkinter import Image
from django.shortcuts import render,redirect, get_object_or_404

from upwork import settings
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login as lg , logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from twilio.rest import Client
from .forms import PhoneNumberVerificationForm


###############################  NEW_REGISTERATION  ########################################

# def register(request):
#     if request.method == "POST": 
#         form = RegisterForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("/")
#     else:
#         form = RegisterForm()
#             # form2=ImageForm()
#     return render(request,"register.html", {"form":form})


def register(request):

    if request.method == 'POST':
        
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            print(password)

            try:
                if CustomUser.objects.filter(username = username).first():
                    messages.success(request, 'Username is taken.')
                    return redirect('/register')

                if CustomUser.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken.')
                    return redirect('/register')
                
                user_obj=form.save()
                user_obj = CustomUser(username = username , email = email)
                # user_obj.set_password(password)
                # user_obj.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
                profile_obj.save()
                # form.save()
                send_mail_after_registration(email , auth_token)
                # return redirect('/token',locals())
            except Exception as e:
                print(e)
                send_mail_after_registration(email , auth_token)
            return redirect('/token',locals())


    else:
        form = RegisterForm()
        # form2=ImageForm()
    return render(request,"register.html",locals())

def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')




def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


#################################### LOG_IN ################################################

# from django.contrib.auth import authenticate, login
# from django.contrib.auth.views import *
# from django.shortcuts import render, redirect
# from .forms import *
# from django.contrib import messages

# def login(request):
#     if request.method == 'POST':
#         form = loginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             print(username,password,"kkkkkkkkkkkkkkkkkkkkkkkkkkk")
#             data = CustomUser(username = username , password = password)
#             print(data.username,data.password)
#             user = authenticate(data)
#             print(user)
            
#             if user is not None:
#                 if user.profile.is_verified:  # Assuming you have a 'profile' attribute in your CustomUser model
#                     lg(request, user)
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'Profile is not verified. Check your email.')
#             else:
#                 messages.error(request, 'Invalid credentials. Please try again.')

#     else:
#         form = loginForm()

#     return render(request, 'login.html', {'form': form})

# def login(request):
#     if request.method =='POST': 
#         form = loginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             print(username,password,"hhhhhhhhhhhhhhhhhh")
#             # user = authenticate(request, username=username, password=password)
#             # print(user, "kkkkkkkkkkkkkkkkkkkkkkkkkk")
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 lg(request, user)
#                 return redirect('home')
#             else:
#                 print("Authentication failed. Invalid credentials.")
#     else:
#         form = loginForm()
#     return render(request, 'login.html',locals())




def login(request):
    
    if request.method == 'POST':
        form=loginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = CustomUser.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/')
        if user is not None:
            lg(request , user)
            return redirect('home')

    else:
        form=loginForm
        # print("error")
    return render(request,'login.html',locals())

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # user_obj = form.save() 
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            print(password)

            try:
                if CustomUser.objects.filter(username = username).first():
                    messages.success(request, 'Username is taken.')
                    return redirect('/register')

                if CustomUser.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken.')
                    return redirect('/register')
                
                user_obj = form.save() 
                # user_obj.set_password(password)
                # user_obj.save()
                auth_token = str(uuid.uuid4())
                expires_at = timezone.now() + timezone.timedelta(minutes=1)
                profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token,expires_at=expires_at)
                profile_obj.save()
                send_mail_after_registration(email , auth_token)
            except Exception as e:
                print(e)
                send_mail_after_registration(email , auth_token)
            return redirect('/token')
    else:
        form = RegisterForm()
    return render(request, "register.html", locals())

def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.expires_at>=timezone.now():
                if profile_obj.is_verified:
                    messages.success(request, 'Your account is already verified.')
                    return redirect('/login_view')
                else:
                    return redirect('/error')
            else:
                HttpResponse("verification cancel")
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, 'Your account has been verified.')
        return redirect('view')
        # else:
        #     return redirect('/error')
    except Exception as e:
        print(e)
    return redirect('/')

def error_page(request):
    return  render(request ,'error.html')



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
################################# LOG_OUT #################################################

def log_out(request):
    logout(request)
    return redirect('/')
###############################  DELETE_PROJECT ############################################

def delete(request, id):
      member = project.objects.filter(id=id)
      member.delete() 
      return redirect('home')
     
################################ HOME_PAGE ##############################################
@login_required
def home(request):
    user = request.user 
    user_id=user.id
    data=project.objects.filter(created_by=user_id)
    data1=project.objects.all()
    img = CustomUser.objects.filter(id=user_id)
    imgs = Images.objects.filter(user_id = request.user.id)
    img2 = imgs.last()


    print(data1)
    return render(request,"homepage.html",locals())

####################### SHOW_PROPOSAL#######################################################

def show_proposal(request,id):
    user_id = CustomUser.objects.all()
    data=proposal.objects.filter(project_id=id)
    request.session['proj_id']=id
    return render(request,"show_proposal.html",locals())
    

############################### ADD_PROPOSAL #################################################

def add_proposal(request,id):
    if request.method =='POST':
        form = proposalForm(request.POST)
        if form.is_valid():
            pro=project.objects.get(id=id)
            profile = form.save(commit=False)
            profile.freelancer=request.user
            profile.project=pro
            profile.save()
            return redirect("home")
    else:
        form = proposalForm()
    return render(request,"add_proposal.html",locals())

################################ PROPOSAL_STATUS ############################################

def proposal_status(request):
    user = request.user
    id = user.id
    data = proposal.objects.filter(freelancer_id=id)
    return render(request,"proposal_status.html",locals())

########################### ADD_PROJECT ###################################################

def add_project(request):
    if request.method =='POST':
        form = projectForm(request.POST)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.created_by=request.user
            pro.save()
            return redirect("home")
    else:
        form = projectForm()
        return render(request,"add_project.html",locals())

################################# PROJECT_UPDATE  ##########################################

def update(request,id):
    mymember = project.objects.get(id=id)
    template = loader.get_template('update.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context,request))



def updaterecord(request,id):
    title = request.POST['title']
    descreption = request.POST['descreption']
    budget = request.POST['budget']
    member = project.objects.get(id=id)
    member.title = title
    member.descreption = descreption
    member.budget = budget
    member.save()
    return redirect('home')


 #############################  PRPOPOSAL_STATUS #############################################

def accept_request(request,id):
    proposal_id = id
    accept= request.POST["accept"]
    proposals= proposal.objects.filter(id=proposal_id).last()
    proposals.status = accept
    proposals.save()
    return redirect('home')

def reject_request(request,id):
    proposal_id = id
    reject= request.POST["reject"]
    proposals= proposal.objects.filter(id=proposal_id).last()
    proposals.status = reject
    proposals.save()
    return redirect('home')

############################### MESSAGES ##############################################

def message(request,id):
    chat=id
    user=request.user.user_type
    if request.method =='POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.sender_type=user
            pro.receiver_id=chat
            pro.sender_id=request.user.id
            pro.save()
            return redirect("proposal_status")  
    else:
        form=MessageForm()
    return render(request,"message.html",locals()) 
    
def check_msg(request,id):
    id = request.user.id
    project_id=id
    msg = Message.objects.filter(Receiver_id=id)
    return render(request,"message_list.html",locals())


def check_msg2(request,id):
    id = request.user.id
    project_id=id
    msg =Message.objects.filter(receiver_id=id)
    return render(request,"message_list2.html",locals())




def message2(request ,id):
    chat=id
    user=request.user.user_type
    if request.method =='POST':
        form = MessageForm2(request.POST)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.sender_type=user
            pro.sender_id=request.user.id
            pro.receiver_id=chat 
            pro.save()
            return redirect("home")  
    else:
        form = MessageForm2()
        return render(request,"message.html",locals())
        


def freelancers_list(request):
    freelancer = CustomUser.objects.all()
    return render(request,"freelancers_list.html",locals())



def clint_msg(request ,id):
    chat=id
    user=request.user.user_type
    if request.method =='POST':
      
        form = MessageForm2(request.POST)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.sender_type=user
            pro.sender_id=request.user.id
            pro.receiver_id=chat 
          
            pro.save()
           
            return redirect("freelancers_list")  
    else:
        form = MessageForm2()
        return render(request,"message.html",locals())
        


def chat_board(request,id):
    client = id
    print(client)
    login_id = request.user.id
    sender_chat = Message.objects.filter((Q(sender_id=login_id) & Q(receiver_id=client) | Q(sender_id=client) & Q(receiver_id=login_id))).order_by('created_at')
    print(sender_chat)
    user = request.user.user_type
    if request.method =='POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            profile= form.save(commit=False)
            profile.sender_user = user
            profile.sender_id = request.user.id
            profile.receiver_id = client  
            profile.save()
            return redirect("chat_board",id=client)  
    else:
        form=MessageForm()
        return render(request,"chatbot.html",locals()) 


def inbox(request):
    user=request.user.id
    data=Message.objects.filter(receiver_id=user)
    return render(request,"inbox.html",locals())

    
    ########################## UPDATE_PROFILE ################# ##############################
def update_profile(request,id):
    img = CustomUser.objects.get(id=id)
    template = loader.get_template('update_profile.html')
    context = {
        'img': img,
    }
    return HttpResponse(template.render(context,request))

    ########################### save profile ################################################
def profile_save(request,id):
    imagess = request.FILES['image']
    member = CustomUser.objects.get(id=id)
    member.image = imagess
    member.save()
    return redirect('home')




@login_required
def my(request):
    if request.method == 'POST':
        form = PicturesForm(request.POST, request.FILES)
        if form.is_valid():
            user_images = Images.objects.filter(user=request.user).count()
            if user_images < 5:
                new_image = form.save(commit=False)
                new_image.user = request.user
                new_image.save()
                
                username = request.user.username
                # Assuming 'files' is the name of the file field in your form
                uploaded_image = request.FILES['files']
                user_folder_path = os.path.join("media","images", username)
                os.makedirs(user_folder_path, exist_ok=True)

                image_path = os.path.join(user_folder_path, uploaded_image.name)
                with open(image_path, 'wb+') as destination:
                    for chunk in uploaded_image.chunks():
                        destination.write(chunk)
            return redirect("home")  # Redirect after successful image upload

    else:
        form = PicturesForm()
    
    return render(request, 'add_image.html', {'form': form})



#####################     Mobile_number_verification   ##############################

def verify_phone_number(request):
    user = request.user
    phone_number = request.POST.get("phone_number")
    print(phone_number)
    if phone_number:
        phone_number = '+91'+phone_number
    if request.method == 'POST':
        if Mobile.objects.filter(phone_number=phone_number):
            return HttpResponse("this number is already exist")
        code = generate_verification_code()
        form = PhoneNumberVerificationForm(request.POST, instance=user)
        data = Mobile.objects.create(phone_number=phone_number,user_id=request.user.id,verification_code=code)
        data.save()
        send_verification_code(phone_number,code)
        messages.success(request, 'Verification code sent successfully.')
        return render(request,"otp.html")
    else:
        form = PhoneNumberVerificationForm(instance=user)

    return render(request, 'verify_phone_number.html', locals())

def generate_verification_code():
    # Generate a 6-digit random verification code
    import random
    code = random.randint(111111,999999)
    return code

def send_verification_code(phone_number, code):
    account_sid = 'ACc619a84d767712f652bc4657f2908ecf'
    auth_token = '8f588e7333c91acf5842b7b960eb2335'
    twilio_number = '+12028836286'

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=str(phone_number),
        from_=twilio_number,
        body=f'Your verification code is: {code}'
    )

def verify_otp(request):
    user = request.user.id
    code = request.POST.get("otp")
    print(code,"hhhhhhhhhhhhhhhhhhh")
    otp = Mobile.objects.get(user_id = user)
    print(otp.verification_code,"gggggggggggggggg")
    if otp.verification_code == code:
        
        otp.is_phone_verified = True
        otp.save()

    return redirect("home")
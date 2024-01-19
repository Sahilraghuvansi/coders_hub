from django.urls import path
from . import views



urlpatterns = [
    path('',views.login, name='login'),
    path('register/',views.register, name='register'),
    
    path('add_project',views.add_project, name='add_project'),
    path('add_proposal/<int:id>',views.add_proposal, name='add_proposal'),
    path('home',views.home, name='home'),
    path('log_out',views.log_out, name='log_out'),
    path('delete/<int:id>',views.delete, name='delete'),
    path('show_proposal/<int:id>',views.show_proposal, name='show_proposal'),
    path('update/updaterecord/<int:id>',views.updaterecord, name='updaterecord'),
    path('update/<int:id>',views.update, name='update'),
    path('proposal_status',views.proposal_status, name='proposal_status'),
    path('accept_request/<int:id>', views.accept_request, name='accept_request'),
    path('reject_request/<int:id>', views.reject_request, name='reject_request'),


    path('message/<int:id>',views.check_msg2, name='check_msg2'),
    path('mesg/<int:id>',views.message, name='message'),

    # path('message1/<int:id>', views.check_msg1, name='check_msg1'),
    path('message2/<int:id>', views.message2, name='message2'),
    path('freelancers_list', views.freelancers_list, name='freelancers_list'    ),
    path('msg/<int:id>',views.chat_board, name='chat_board'),
    


    path('message1/<int:id>', views.check_msg2, name='check_msg2'),
    path('message1/<int:id>', views.chat_board, name='chat_board'),

    path('reply/<int:id>',views.chat_board, name='chat_board'),
    path('update_profile/<int:id>', views.update_profile, name='profile_update'),
    path('update_profile/profile_save/<int:id>', views.profile_save, name='profile_save'),
    path('inbox' , views.inbox , name="inbox"),
    path('token' , views.token_send , name="token_send"),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),
   
    path('my/', views.my, name='my'),



    path('verify_phone_number/', views.verify_phone_number, name='verify_phone_number'),

    path('verify_otp', views.verify_otp, name='verify_otp'),


]



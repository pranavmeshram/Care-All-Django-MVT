from django.urls import path
from care_all.views import *


urlpatterns = [
    # ************************************** General Functionalities URLs *******************************************************
    path('', home_view, name='home_page'),
    path('my-profile/<int:pk>', show_profile_view, name='show_profile_page'),

    path('make-donation', make_donation_view, name='make_donation_page'),
    path('privacy-policy', privacy_policy_view, name='privacy_policy_page'),

    path('contact-us', contact_us_view.as_view(),  name="contact_us_page"),
    path('thank-you', thank_you_view,  name="thank_you_page"),


    # ************************************** Elder Functionalities URLs *********************************************************
    path('edit-E-profile/<int:pk>', edit_elder_profile_view.as_view(), name='edit_elder_profile_page'),

    path('care-request-in-your-queue/', care_request_queue_view, name='care_request_queue_page'),    
    path('care-request-sender-profile/<int:pk>', care_request_sender_profile_view, name='care_request_sender_profile_page'),

    path('set-funds/<int:pk>', set_funds_view.as_view(), name='set_funds_page'),
    
    path('approve-care-request/<int:pk>', approve_care_request_view.as_view(), name='approve_care_request_page'),



    # ************************************** Youngster Functionalities URLs ******************************************************
    path('edit-Y-profile/<int:pk>', edit_youngster_profile_view.as_view(), name='edit_youngster_profile_page'),

    path('available-elders/', show_available_elders_view.as_view(), name='show_available_elders_page'),
    path('un-available-elders/', show_un_available_elders_view.as_view(), name='show_un_available_elders_page'),

    path('available-elders-profile/<int:pk>', available_elders_profile_view, name='available_elders_profile_page'),

    path('send-care-request/<int:pk>', send_care_request_view.as_view(), name='send_care_request_page'),

    path('elder-in-your-care/', elder_in_care_view, name='elder_in_care_page'),

    path('my-earnings/', my_earnings_view, name='my_earnings_page'),  

]   
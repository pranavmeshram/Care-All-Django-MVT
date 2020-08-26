from django.urls import path, include
from accounts.views import sign_up_view

urlpatterns = [
    path('sign-up/', sign_up_view.as_view(), name='signup_page'), 
    path("", include("django.contrib.auth.urls")),

]

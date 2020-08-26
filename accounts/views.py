from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import CreateView
from django.conf import settings
from accounts.forms import SignupForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login


# Create your views here.

class sign_up_view(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        initial_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=initial_password)
        login(self.request, user)
        return redirect('home_page')
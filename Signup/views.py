from django.shortcuts import render, redirect
from django.contrib import messages
#from . import urls
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        first_name = form.cleaned_data.get('Email_ID')
        last_name = form.cleaned_data.get('Institute_Name')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
        context = {'form': form}
    return render(request, 'registration/login.html', context)

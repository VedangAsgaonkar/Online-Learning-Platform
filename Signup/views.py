from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def signup_view(request):
    form = SignUpForm(request.POST)
    # print(form.is_valid())
    # print(form.cleaned_data.get('username'), form.cleaned_data.get('password1'),form.cleaned_data.get('password2'),form.cleaned_data.get('Email_ID'),form.cleaned_data.get('Institute_Name'))
    if form.is_valid():
        # print("++++++++++")
        user = form.save()
        user.refresh_from_db()
        user.member.email_id = form.cleaned_data.get('Email_ID')
        user.member.institute_name = form.cleaned_data.get('Institute_Name')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)       
        login(request, user)
        return redirect('signup')
    else:
        # print("=============")
        form = SignUpForm()
        context = {'form': form}
    return render(request, 'registration/signup.html', context)

'''
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})
'''








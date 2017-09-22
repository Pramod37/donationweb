# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from daandoo.settings import BASE_DIR
from django.shortcuts import render,redirect
from forms import SignUpForm , LoginForm
from django.contrib.auth.hashers import make_password, check_password
from models import UserModel,SessionToken
# Create your views here.

def signup_view(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if (len(form.cleaned_data['username']) < 5 or set('[~!#$%^&*()_+{}":;\']+$ " "').intersection(form.cleaned_data['username'])):
                return render(request, 'invalid.html')
            else:
                if (len(form.cleaned_data["password"]) > 5):
                    username = form.cleaned_data['username']
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    user = UserModel(name=name, password=make_password(password), email=email, username=username)
                    user.save()

                    return render(request, 'success.html')
                else:
                    form = SignUpForm()
    elif request.method == "GET":
        form = SignUpForm()

    return render(request, 'index.html', {'form': form})


def login_view(request):
    response_data={}
    if request.method == "POST":

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()
            if user:
                if check_password(password,user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('login/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'
    elif request.method == "GET":

        form = LoginForm()
        response_data['form'] = form
        return render(request, 'login.html')


#def main_view(request):


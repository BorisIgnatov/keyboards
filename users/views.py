from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from keyboard.views import home

def signup_page(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirmation']:
            try:
                user = User.objects.create_user(request.POST['email'],
                                                password=request.POST['password'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.save()
                login(request,user)
                return redirect(home)
            except IntegrityError:
                return render(request,'signup.html',{'error':'This email is already used'})
        else:
            return render(request,'signup.html',{'error':'Passwords are not matching'})


def login_page(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect(home)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect(home)

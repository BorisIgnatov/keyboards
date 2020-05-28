from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Avg
from django.contrib.auth import login, logout, authenticate
from .models import *


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


def home(request):
    keyboards = Keyboard.objects.all()
    if request.method == 'GET':
        return render(request, 'home.html', {'keyboards':keyboards})
    elif request.method == 'POST':
        if request.POST.get('price'):
            return render(request,'home.html',{'keyboards':keyboards.order_by('price')})
        elif request.POST.get('rating'):
            return render(request,'home.html',{'keyboards':keyboards.order_by('-rating')})
        elif request.POST.get('date'):
            return render(request,'home.html',{'keyboards':keyboards})


def brands(request):
    brands = Brand.objects.all()
    return render(request, 'brands.html',{'brands':brands})


def switches(request):
    switches = Switch.objects.all()
    return render(request, 'switches.html',{'switches':switches})


def detail_keyboard(request,keyboard_id):
    keyboard = get_object_or_404(Keyboard,pk=keyboard_id)
    reviews = Review.objects.all().filter(keyboard=keyboard.id)
    keyboard_rating = round(keyboard.rating,2)
    try:
        reviews_count = reviews.count()
        pos_count = reviews.filter(is_positive=True).count()
        neg_count = reviews.filter(is_positive=False).count()
    except Exception as e:
        reviews_count = 0
        pos_count = 0
        neg_count = 0

    if request.method == 'GET':
        return render(request, 'detail_keyboard.html',{'keyboard':keyboard,
                                                      'reviews':reviews,
                                                      'count':reviews_count,
                                                      'pos_count':pos_count,
                                                      'neg_count':neg_count})
    elif request.method == 'POST':
        if request.user:
            review = Review(user=request.user,keyboard=keyboard,
                            rating=request.POST.get('rating'),
                            content=request.POST.get('content'),
                            is_positive=request.POST.get('is_positive') == 'True')

            review.save()
            keyboard.rating = reviews.aggregate(Avg('rating'))['rating__avg']
            keyboard.save()
            return render(request, 'detail_keyboard.html',{'keyboard':keyboard,
                                                            'reviews':reviews,
                                                            'count':reviews_count,
                                                            'pos_count':pos_count,
                                                            'neg_count':neg_count})
        else:
            redirect(signup)


def detail_brand(request,brand_id):
    brand = get_object_or_404(Brand,pk=brand_id)
    keyboards = Keyboard.objects.filter(brand_name=brand)
    return render(request, 'detail_brand.html',{'brand':brand, 'keyboards':keyboards})


def detail_switch(request,switch_name):
    switch = get_object_or_404(Switch,name=switch_name)
    return render(request, 'detail_switch.html',{'switch':switch})


def search(request):
    brands = Brand.objects
    keyboards = Keyboard.objects
    switches = Switch.objects
    if request.method == 'GET':
        return render(request,'search.html',{'keyboards':keyboards.all(),
                                            'switches':switches.all(),
                                            'brands':brands.all()})
    elif request.method == 'POST':
        try:
            if request.POST.get('switches'):
                key_list = Brand.objects.none()
                for i in request.POST.getlist('switches'):
                    key_list = key_list | keyboards.filter(switches__name__contains=i)
                keyboards = key_list

            if request.POST.get('brands'):
                key_list = Brand.objects.none()
                for i in request.POST.getlist('brands'):
                    key_list = key_list | keyboards.filter(brand_name__name__contains=i)
                keyboards = key_list

            if request.POST.get('priceMin'):
                min = request.POST.get('priceMin')
                keyboards = keyboards.filter(price__gte=min)

            if request.POST.get('priceMax'):
                max = request.POST.get('priceMax')
                keyboards = keyboards.filter(price__lte=max)

            if request.POST.get('keyboard_name'):
                try:
                    key_list = Brand.objects.none()
                    key_list = key_list | keyboards.filter(model_name__icontains=request.POST.get('keyboard_name'))
                    keyboards = key_list
                except Exception as e:
                    match_error = e

            return render(request,'search.html',
                         {'keyboards':keyboards.all(),
                         'switches':switches.all(),
                         'brands':brands.all(),
                         'match_error':match_error})
        except Exception as e:
            return render(request,'search.html',{'keyboards':keyboards.all(),
                                                'switches':switches.all(),
                                                'brands':brands.all(),
                                                'error':e})

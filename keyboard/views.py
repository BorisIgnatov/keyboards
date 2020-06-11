from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Avg
from django.contrib.auth import login, logout, authenticate
from .models import *
from .services.review import review
from .services.search import search


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
            review(request, keyboard)
            keyboard.rating = reviews.aggregate(Avg('rating'))['rating__avg']
            return render(request, 'detail_keyboard.html',{'keyboard':keyboard,
                                                          'reviews':reviews,
                                                          'count':reviews_count,
                                                          'pos_count':pos_count,
                                                          'neg_count':neg_count})
        else:
            redirect('signup_page')


def detail_brand(request,brand_id):
    brand = get_object_or_404(Brand,pk=brand_id)
    keyboards = Keyboard.objects.filter(brand_name=brand)
    return render(request, 'detail_brand.html',{'brand':brand, 'keyboards':keyboards})


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
                    keyboards = keyboards.filter(switches__name__contains=i)

            if request.POST.get('brands'):
                key_list = Brand.objects.none()
                for i in request.POST.getlist('brands'):
                    keyboards = keyboards.filter(brand_name__name__contains=i)

            if request.POST.get('priceMin'):
                min = request.POST.get('priceMin')
                keyboards = keyboards.filter(price__gte=min)

            if request.POST.get('priceMax'):
                max = request.POST.get('priceMax')
                keyboards = keyboards.filter(price__lte=max)

            if request.POST.get('keyboard_name'):
                try:
                    keyboards = keyboards.filter(model_name__icontains=request.POST.get('keyboard_name'))
                except Exception as e:
                    match_error = e

            return render(request,'search.html',
                         {'keyboards':keyboards.all(),
                         'switches':switches.all(),
                         'brands':brands.all()})
        except Exception as e:
            return render(request,'search.html',{'keyboards':keyboards.all(),
                                                'switches':switches.all(),
                                                'brands':brands.all(),
                                                'error':e})

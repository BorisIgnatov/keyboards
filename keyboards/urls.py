"""keyboards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from keyboard.views import *
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name='home'),
    path('signup', signup_page,name='signup'),
    path('login', login_page,name='login'),
    path('logout', logout_view,name='logout'),
    path('brands', brands,name='brands'),
    path('keyboards/<int:keyboard_id>', detail_keyboard,name='detail_keyboard'),
    path('brands/<int:brand_id>', detail_brand,name='detail_brand'),
    path('search', search,name='search'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

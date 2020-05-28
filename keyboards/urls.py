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
from keyboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('signup', views.signup_page,name='signup'),
    path('login', views.login_page,name='login'),
    path('brands', views.brands,name='brands'),
    path('switches', views.switches,name='switches'),
    path('keyboards/<int:keyboard_id>', views.detail_keyboard,name='detail_keyboard'),
    path('brands/<int:brand_id>', views.detail_brand,name='detail_brand'),
    path('switches/<str:switch_name>', views.detail_switch,name='detail_switch'),
    path('search', views.search,name='search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

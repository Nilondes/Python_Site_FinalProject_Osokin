"""
URL configuration for clothing_rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from clothing_rental import settings
from django.contrib import admin
from django.urls import path
from app.views import (register,
                       user_login,
                       home,
                       about,
                       contact,
                       create_ad,
                       pending_ads,
                       approve_ad,
                       user_logout,
                       view_user_ads,
                       remove_ad,
                       edit_ad,
                       search_ads,
                       view_ad,
                       pending_comments,
                       approve_comment,
                       order_ad)


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create_ad/', create_ad, name='create_ad'),
    path('approve_ad/', pending_ads, name='pending_ads'),
    path('approve_ad/<int:pk>', approve_ad, name='approve_ad'),
    path('user_ads/', view_user_ads, name='user_ads'),
    path('user_ads/<int:pk>', edit_ad, name='edit_ad'),
    path('remove_ad/<int:pk>', remove_ad, name='remove_ad'),
    path('search_ads/', search_ads, name='search_ads'),
    path('search_ads/<int:pk>', view_ad, name='view_ad'),
    path('search_ads/<int:pk>/order_ad', order_ad, name='order_ad'),
    path('pending_comments/', pending_comments, name='pending_comments'),
    path('pending_comments/<int:pk>', approve_comment, name='approve_comment'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
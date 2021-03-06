"""myrecommendationsystem URL Configuration

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
from pages import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('recommend/content/',views.recommended,name='content'),
    path('backend/', admin.site.urls),
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.loginuser,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('<int:place_id>/', views.rating, name='rating'),
    path('recommend/',views.recommend,name='recommend'),
    path('details/',views.detail,name='detail'),
    path('<int:pk>/info/',views.Detail.as_view(),name='detailhome'),
    
]


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
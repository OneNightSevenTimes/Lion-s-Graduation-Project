"""competition_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url('index/$', views.Homepage.as_view()),
    url(r'^administratorlogin/', views.administratorlogin),
    url(r'^administrator/', views.administrator),
    url(r'^index/check_code.html$', views.CheckCodeView.as_view()),
    url(r'^register/check_code.html$', views.CheckCodeView.as_view()),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^user_protocol/$', views.UserProtocolView.as_view()),
]

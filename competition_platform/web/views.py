from django.views import View
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from web.models import AdministratorInfo
# Create your views here.


class Homepage(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        err_msg = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        res = redirect(request.GET.get('next') if request.GET.get('next') else "/index.html")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return res
        else:
            err_msg['error'] = '用户名密码错误!'
            return render(request,'login.html',{'error':err_msg})


class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("/login/")


def administratorlogin(request):
    print("ffffffffffffffff")
    if request.method == 'GET':
        return render(request, 'index.html')
        print("aaaaaaaaaaaaaaaaaa")
    elif request.method == 'POST':
        phone = request.POST.get('ad_phone')
        password = request.POST.get('ad_password')
        user = AdministratorInfo.objects.filter(ad_phone__exact=phone, ad_password__exact=password)
        if user:
            response = HttpResponseRedirect('/administrator/')
            response.set_cookie('username', 3600)
            return response
        else:
            return render(request, 'index.html')


def administrator(request):
    return render(request, 'administrator.html')




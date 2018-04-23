from django.views import View
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from web.models import AdministratorInfo
from web.utils import check_code
from io import BytesIO
import json
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from repository import models
from django.core.exceptions import ValidationError
# Create your views here.


class Homepage(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'index.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        result= {'err_msg':{},'status':'False'}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
            pass
        else:
            result['err_msg']['error'] = '验证码错误'
            return HttpResponse(json.dumps(result))
        if user:
            login(request, user)
            result['status'] = 'True'
        else:
            result['err_msg']['error'] = '用户名密码错误!'
        return HttpResponse(json.dumps(result))



class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("/index/")


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


class CheckCodeView(View):
    def get(self,request,*args,**kwargs):
        stream = BytesIO()
        img, code = check_code.create_validate_code()
        img.save(stream, 'PNG')
        request.session['CheckCode'] = code
        return HttpResponse(stream.getvalue())

# class RegisterView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,'UserRegister.html')

class UserProtocolView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'user_protocol.html')

class RegisterForm(Form):
    username = fields.CharField(
        error_messages={"required":"用户名不能为空"},
        widget=widgets.TextInput(attrs={'id': 'username', 'class': 'username','placeholder':'请输入用户名'})
    )
    pwd = fields.CharField(
        min_length=6,
        max_length=12,
        error_messages={'required':'密码不能为空','min_length':'密码长度不能小于6','max_length':'密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'pwd','id':'pwd','placeholder':'密码长度6-16位，数字、字母'}, render_value=True)
    )
    repwd = fields.CharField(
        min_length=6,
        max_length=12,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'repwd','id':'repwd','placeholder':'请再次输入您的密码'}, render_value=True)
    )
    vcode = fields.CharField(
        error_messages={'required': '验证码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': 'code-input fl','id':'vcode','placeholder':'请输入验证码'}, render_value=True)
    )

    def clean_username(self):
        c = models.UserProfile.objects.filter(username=self.cleaned_data['username']).count()
        if not c:
            return self.cleaned_data['username']
        else:
            raise ValidationError('用户名已经存在', code='xxx')


    def clean_repwd(self):
        if self.cleaned_data['repwd'] == self.cleaned_data['pwd']:
            return self.cleaned_data['repwd']
        else:
            raise ValidationError('两次密码输入不一致', code='xxx')

    def clean(self):
        return self.cleaned_data


class RegisterView(View):
    def get(self,request,*args,**kwargs):
        obj = RegisterForm()
        return render(request, 'UserRegister.html', {'form': obj})

    def post(self,request,*args,**kwargs):
        obj = RegisterForm(request.POST)
        print(obj.errors)
        if request.session['CheckCode'].upper() == request.POST.get('vcode').upper():
            pass
        elif  request.POST.get('vcode'):
        #     # obj.errors.vcode[0]="验证码不正确"
            obj.errors['vcode']=['验证码不正确']
        #     return render(request, 'UserRegister.html', {'form': obj})
        if obj.is_valid():
            values = obj.clean()
            name = values['username']
            pwd = values['pwd']
            django_user = models.User.objects.create_user(name,name,pwd)
            django_user.save()
            models.UserProfile.objects.create(username=name,password=pwd)
        else:
            return render(request,'UserRegister.html',{'form':obj})
        return render(request,'index.html')
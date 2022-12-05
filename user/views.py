from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def userRegister(request):
    if request.method == "POST":
        kullanici = request.POST['kullanici']
        email = request.POST['email']
        isim = request.POST['isim']
        soyisim = request.POST['soyisim']
        sifre1 = request.POST['sifre1']
        sifre2 = request.POST['sifre2']

        if sifre1 == sifre2:
            if User.objects.filter(username = kullanici).exists():
                messages.error(request, 'Kullanıcı adı zaten alınmış.')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email zaten kullanımda.')
                return redirect('register')
            elif len(sifre1) < 6:
                messages.error(request, 'Şifre en az 6 karakter olmalıdır')
                return redirect('register')
            else:
                user = User.objects.create_user(username = kullanici, email = email, password = sifre1)
                Hesap.objects.create(
                    user = user,
                    isim = isim,
                    soyisim = soyisim,
                )
                user.save()
                messages.success(request, 'Kayıt başarılı')
                return redirect('index')
        else:
            messages.error(request, 'Şifreler uyuşmuyor')
            return redirect('register')

    return render(request,'user/register.html')

def userLogin(request):
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        sifre = request.POST['sifre1']

        user = authenticate(request, username = kullanici, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş yapıldı')
            return redirect('index')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')
            return redirect('login')
    return render(request, 'user/login.html')

def userLogout(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı')
    return redirect('index')
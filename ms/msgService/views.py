from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'msgService/index.html')


def login_r(request):
    return render(request, 'msgService/login.html')


def register(request):

    return render(request, 'msgService/register.html')
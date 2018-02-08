from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *

# Create your views here.


def home(request):
    """
    home page of website, user not logged in.
    :param request: HTTP request
    :return: home page (index.html)
    """
    return render(request, 'msgService/index.html')


def login_r(request):
    """
    login page
    :param request: HTTP request
    :return: login page
    """
    return render(request, 'msgService/login.html')


class RegisterForm(View):
    """
    Register Form to be displayed
    """
    form = RegisterForm
    template_name = 'msgService/register.html'

    def get(self, request):
        """
        Display blank form
        """
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        """
        Receive and check data
        """
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # user = authenticate(username=username, password=password) #debugging

            if user is not None:
                if user.is_active:
                    return redirect('login')

        return render(request, self.template_name, {'form': form})


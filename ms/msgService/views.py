from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib.auth import authenticate, login, logout

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
    if request.user.is_authenticated():
        logout(request)

    if request == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(username=phone_number, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return render(request, 'msgService/registered/home.html')
            else:
                return render(request, 'msgService/login.html',
                              {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'msgService/login.html',
                          {'error_message': 'Your username/password does not match.'
                                            '<br>Don\'t have an account?'
                                            '<a href="signup">'
                                            'Click here</a> to register.'})

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
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            user.create_user(email, phone_number, password)
            user.save()

            user = authenticate(username=phone_number, password=password)  # debugging

            if user is not None:
                if user.is_active:
                    return redirect('login')

        return render(request, self.template_name, {'form': form})


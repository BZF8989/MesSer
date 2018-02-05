from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *

# Create your views here.


def home(request):
    return render(request, 'msgService/index.html')


def login_r(request):
    return render(request, 'msgService/login.html')


class RegisterForm(View):
    """
    Registration form
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


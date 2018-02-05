from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^login', views.login_r, name='login'),

    url(r'^register', views.RegisterForm.as_view(), name='register'),


]

from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.default_web, name='default_web'),
    url(r'^accounts/login/$', views.login_form, name='login_form'),
    url(r'^accounts/registration/$', views.registration_form, name='registration_form'),
    url(r'^accounts/logout/$', views.logout_form, name='logout_form'),
]

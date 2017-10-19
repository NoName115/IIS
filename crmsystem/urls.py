from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.default_web, name='default_web'),
    url(r'^accounts/login/$', views.login_form, name='login_form'),
    url(r'^accounts/registration/$', views.registration_form, name='registration_form'),
    url(r'^accounts/logout/$', views.logout_form, name='logout_form'),
    url(r'^role_site/$', views.role_site, name='role_site'),
    url(r'^contract/$', views.contract_site, name='contract_site'),
    url(r'^contract/new/$', views.contract_new, name='contract_new'),
    url(r'^meeting/$', views.meeting_site, name='meeting_site'),
    url(r'^meeting/new/$', views.meeting_new, name='meeting_new'),
    url(r'^customer/$', views.customer_site, name='customer_site'),
    url(r'^customer/new/$', views.customer_new, name='customer_new'),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.customer_edit, name='customer_edit'),
    url(r'^worker/$', views.worker_site, name='worker_site'),
    url(r'^worker/new/$', views.worker_new, name='worker_new'),
    url(r'^worker/(?P<pk>\d+)/edit/$', views.worker_edit, name='worker_edit'),
    url(r'^cloth/$', views.cloth_site, name='cloth_site'),
]

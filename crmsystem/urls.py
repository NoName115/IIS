from django.conf.urls import url, include
from . import views


urlpatterns = [
    # Gome page
    url(r'^$', views.default_web, name='default_web'),

    # Account pages
    url(r'^accounts/login/$', views.login_form, name='login_form'),
    url(r'^accounts/registration/$', views.registration_form, name='registration_form'),
    url(r'^accounts/logout/$', views.logout_form, name='logout_form'),

    # Other pages
    url(r'^contract/$', views.contract_site, name='contract_site'),
    url(r'^contract/new/$', views.contract_new, name='contract_new'),
    url(r'^contract/(?P<pk>\d+)/delete$', views.contract_delete, name='contract_delete'),
    url(r'^meeting/$', views.meeting_site, name='meeting_site'),
    url(r'^meeting/new/$', views.meeting_new, name='meeting_new'),
    url(r'^customer/$', views.customer_site, name='customer_site'),
    url(r'^customer/new/$', views.customer_new, name='customer_new'),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.customer_edit, name='customer_edit'),
    url(r'^employee/$', views.employee_site, name='employee_site'),
    url(r'^employee/new/$', views.employee_new, name='employee_new'),
    url(r'^employee/(?P<pk>\d+)/edit/$', views.employee_edit, name='employee_edit'),
    url(r'^cloth/$', views.cloth_site, name='cloth_site'),
    url(r'^cloth/mark/new/$', views.mark_new, name='mark_new'),
    url(r'^cloth/(?P<pk>\d+)/new/$', views.cloth_new, name='cloth_new'),
]

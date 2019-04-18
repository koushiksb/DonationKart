from django.conf.urls import url
from django.urls import path
from . import views

app_name='admin_login'

urlpatterns=[
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]

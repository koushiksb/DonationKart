from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='User'

urlpatterns = [
    path('home/',views.home,name="home"),
    path('events/',views.events,name="events"),
    path('cart/',views.cart,name="cart"),
    path('proceed/',views.proceed,name="proceed"),
    path('delete/<id>',views.delete,name="delete"),
    path('events/<id>',views.filter,name="filter"),
]

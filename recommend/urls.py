from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('result',views.result,name='result'),
]

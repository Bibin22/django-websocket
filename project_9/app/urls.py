from django.urls import path
from .views import *

urlpatterns = [
    path('<str:groupname>/', index, name='index')
]
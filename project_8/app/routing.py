from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/sc/<str:group_name>/', MySyncConsumer.as_asgi()),
    path('ws/ac/<str:group_name>/', MyAsyncConsumer.as_asgi()),
]
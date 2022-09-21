from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('ws/wsc/', MyWebsocketConsumer.as_asgi())
]
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from .models import Chat, Group
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('websocket connected')
        self.send()

    def receive(self, text_data=None, bytes_data=None):
        print('message received from client', text_data)
        self.send(text_data="message from server to client")

    def disconnect(self, close_code):
        print('websocket disconnected', close_code)


from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from .models import Chat, Group
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('websocket connnected', event)
        print('Channel Layer...', self.channel_layer)
        print('Channel name...', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print('group name', self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        print('message recieved', event)
        print('message recieved', event['text'])
        data = json.loads(event['text'])
        print('data', data)
        print('type of data', type(data))
        group = Group.objects.get(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(content=data['msg'],
                        group=group)
            chat.save()
            data['user'] = self.scope['user'].username
            print(data['user'], 'data.user')
            async_to_sync(self.channel_layer.group_send)(
                self.group_name, {
                    'type': 'chat.message',
                    'message':json.dumps(data)
                    # 'message': event['text']
                }
            )

        else:
            self.send({
                'type':'websocket.send',
                'text':json.dumps({'msg':'login required', 'user':'guest'})
            })


    def chat_message(self, event):
        print('Event..', event)
        print('message', event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })


    def websocket_disconnect(self,event):
        print('Websocket Disconnected', event)
        print('Channel Layer...', self.channel_layer)
        print('Channel name...', self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('websocket connnected', event)
        print('Channel Layer...', self.channel_layer)
        print('Channel name...', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print('group name', self.group_name)
        await(self.channel_layer.group_add)(self.group_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('message recieved', event)
        print('message recieved', event['text'])
        data = json.loads(event['text'])
        print('data', data)
        print('type of data', type(data))
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(content=data['msg'],
                        group=group)
            data['user'] = self.scope['user'].username
            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(
                self.group_name, {
                    'type': 'chat.message',
                    'message': json.dumps(data)
                    #'message': event['text']
                }
            )
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'msg': 'login required', 'user':'guest'})
            })



    async def chat_message(self, event):
        print('Event..', event)
        print('message', event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        print('Websocket Disconnected', event)
        print('Channel Layer...', self.channel_layer)
        print('Channel name...', self.channel_name)
        await (self.channel_layer.group_discard)(self.group_name, self.channel_name)
        raise StopConsumer()
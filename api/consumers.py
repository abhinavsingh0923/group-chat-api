from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync



class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('websocket connect..', event)
        print('channel layer..',self.channel_layer)
        print('channel layer name..',self.channel_name)
        chat_channel_name = self.scope['url_route']['kwargs']['channelname']
        async_to_sync (self.channel_layer.group_add)(self.chat_channel_name,self.channel_name)
        self.send({
            'type':'websocket.accept'
        })
    
    def websocket_receive(self, event):
        print('websocket received..',event['text'])
        print('type of message reveived from client...',type(event['text']))
        async_to_sync (self.channel_layer.group_send)(
            self.chat_channel_name,
            {
                'type':'chat.message',
                'message':event['text'],
            }
        )
        # print('event...',event)
    
    def chat_message(self, event):
        print('event...',event)
        print('actural data...',event['message'])
        self.send({
           'type':'websocket.send',
            'text': event['message']
            }
        )

    def websocket_disconnect(self, event):
        print('websocket disconnect..',event)
        print('channel layer..',self.channel_layer)
        print('channel layer name..',self.channel_name)
        async_to_sync (self.channel_layer.group_discard)(self.chat_channel_name,self.channel_name)
        raise StopConsumer()
        
        
 

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('websocket connect..', event)
        chat_channel_name = self.scope['url_route']['kwargs']['channelname']
        async_to_sync (self.channel_layer.group_add)(self.chat_channel_name,self.channel_name)
        await self.send({
            'type':'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        print('websocket recieved..',event)
        print(event['text'])
        async_to_sync (self.channel_layer.group_send)(
            self.chat_channel_name,
            {
                'type':'chat.message',
                'message':event['text'],
            }
        )

    async def chat_message(self, event):
        print('event...',event)
        print('actural data...',event['message'])
        await self.send({
           'type':'websocket.send',
            'text': event['message']
            }
        )

    async def websocket_disconnect(self, event):
        print('websocket disconnect..',event)
        async_to_sync (self.channel_layer.group_discard)(self.chat_channel_name,self.channel_name)
        raise StopConsumer()
 
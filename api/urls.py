from django.urls import path
from . import consumers

urlpatterns = [
    
]

websocket_patterns=[
    path('ws/sc/<str:channelname>',consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:channelname>',consumers.MyAsyncConsumer.as_asgi())
]
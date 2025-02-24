from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class AsyncWebsocketConsumer(AsyncWebsocketConsumer):
    pass


get_channel_layer = get_channel_layer

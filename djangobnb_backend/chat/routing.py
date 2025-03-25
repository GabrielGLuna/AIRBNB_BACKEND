from django.urls import path

from . import  consumers

websocket_urlpatterns = [
    path('ys/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
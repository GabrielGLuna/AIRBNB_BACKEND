from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversations_list, name='api_conservations_list'),
    path('<uuid:pk>/', api.conversations_detail,  name='api_conversations_detail')
]
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer

from useraccount.models import User

from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
def conversations_list(request):
    try:
        serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def conversations_detail(request, pk):
    try:
        conversation = request.user.conversations.get(pk=pk)
        conversation_serializer = ConversationDetailSerializer(conversation, many=False)
        messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)

        return JsonResponse({
            'conversation': conversation_serializer.data,
            'messages': messages_serializer.data
        }, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def conversations_start(request, user_id):
    try:
        conversations = Conversation.objects.filter(users__in=[user_id]).filter(users__in=[request.user.id])

        if conversations.exists():
            conversation = conversations.first()
            return JsonResponse({'success': True, 'conversation_id': conversation.id})
        else:
            user = User.objects.get(pk=user_id)
            conversation = Conversation.objects.create()
            conversation.users.add(request.user)
            conversation.users.add(user)

            return JsonResponse({'success': True, 'conversation_id': conversation.id})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication




from .forms import PropertyForm
from .models import Property
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer

@api_view(['GET'])
@authentication_classes([])  # Si no necesitas autenticación
@permission_classes([])  # Si no necesitas permisos
def properties_list(request):
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)
    return Response({'data': serializer.data})

@api_view(['GET'])
@authentication_classes([])  # Si no necesitas autenticación
@permission_classes([])  
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)

    return JsonResponse(serializer.data)


@api_view(['POST', 'FILES'])
def create_property(request):
    try:
         # Verifica si la imagen fue recibida
        if 'image' in request.FILES:
            print('Imagen recibida:', request.FILES['image'])
        else:
            print('No se recibió ninguna imagen')
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property = form.save(commit=False)
            
            property.landlord = request.user if request.user.is_authenticated else None
            print(request.user)
            property.save()

            return JsonResponse({'success': True}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

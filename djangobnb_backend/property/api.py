from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Property
from .serializers import PropertiesListSerializer

@api_view(['GET'])
@authentication_classes([])  # Si no necesitas autenticación
@permission_classes([])  # Si no necesitas permisos
def properties_list(request):
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)

    return Response({
        'data': serializer.data
    })

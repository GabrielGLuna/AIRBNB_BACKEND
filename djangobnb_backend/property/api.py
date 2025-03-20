from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication




from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationListSerializer

@api_view(['GET'])
@authentication_classes([])  # Si no necesitas autenticación
@permission_classes([])  # Si no necesitas permisos
def properties_list(request):
    properties = Property.objects.all()
    landlord_id = request.GET.get('landlord_id', '')
    if landlord_id:
        properties = properties.filter(landlord_id=landlord_id)
    serializer = PropertiesListSerializer(properties, many=True)
    return Response({'data': serializer.data})

@api_view(['GET'])
@authentication_classes([])  
@permission_classes([])  
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)
    serializer = PropertiesDetailSerializer(property, many=False)

    return JsonResponse(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])  
def property_reservations(request, pk):
    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()
    serializer = ReservationListSerializer(reservations, many=True)

    return JsonResponse(serializer.data, safe=False)

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

@api_view(['POST'])
def book_property(request, pk):
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')

        property = Property.objects.get(pk=pk)

        Reservation.objects.create(
            property = property,
            start_date = start_date,
            end_date = end_date,
            number_of_nights = number_of_nights,
            total_price = total_price,
            guests = guests,
            created_by = request.user
        )
        return JsonResponse({'success':True})
    except Exception as e:
        print('Error', e)

        return JsonResponse({'succes':False})
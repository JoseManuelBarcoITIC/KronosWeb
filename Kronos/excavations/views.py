from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Excavations, Sectors
from .serializers import ExcavationSerializer, SectorSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Excavations, Sectors
from .serializers import ExcavationSerializer, SectorSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def excavation_list(request):
    user = request.user

    if request.method == 'GET':
        excavations = Excavations.objects.filter(
            (Q(owner=user) | Q(users=user)) & Q(is_active=True)
        ).distinct()
        serializer = ExcavationSerializer(excavations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExcavationSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid():
                # El serializador maneja el owner de manera interna gracias al HiddenField
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as database_error:
            # Si el modelo tiene campos distintos o falta una migración, lo capturamos aquí
            return Response(
                {"error_interno_django": str(database_error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def excavation_detail(request, pk):
    try:
        excavation = Excavations.objects.get(pk=pk, is_active=True)
        if excavation.owner != request.user and request.user not in excavation.users.all():
            return Response({"error": "No tienes permiso"}, status=status.HTTP_403_FORBIDDEN)
    except Excavations.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExcavationSerializer(excavation)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ExcavationSerializer(excavation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        excavation.is_active = False
        excavation.save()
        return Response({"message": "Excavación desactivada"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sector_list(request):
    if request.method == 'GET':
        sectors = Sectors.objects.filter(
            (Q(excavation__owner=request.user) | Q(excavation__users=request.user)) &
            Q(is_active=True)
        ).distinct()
        serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def sector_detail(request, pk):
    try:
        sector = Sectors.objects.get(pk=pk, is_active=True)
        excavation = sector.excavation
        if excavation.owner != request.user and request.user not in excavation.users.all():
            return Response(
                {"error": "No tienes permiso para acceder a los sectores de esta excavación"},
                status=status.HTTP_403_FORBIDDEN
            )
    except Sectors.DoesNotExist:
        return Response({"error": "Sector no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SectorSerializer(sector)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = SectorSerializer(sector, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sector.is_active = False
        sector.save()
        return Response(
            {"message": "Sector desactivado correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def excavation_detail(request, pk):
    try:
        excavation = Excavations.objects.get(pk=pk, is_active=True)
        if excavation.owner != request.user and request.user not in excavation.users.all():
            return Response({"error": "No tienes permiso"}, status=status.HTTP_403_FORBIDDEN)
    except Excavations.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExcavationSerializer(excavation)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = ExcavationSerializer(excavation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        excavation.is_active = False
        excavation.save()
        return Response({"message": "Excavación desactivada"}, status=status.HTTP_204_NO_CONTENT)


# --- ESTA ES LA FUNCIÓN QUE TE FALTABA ---
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sector_list(request):
    if request.method == 'GET':
        # Listamos solo los sectores de excavaciones donde el usuario participa
        sectors = Sectors.objects.filter(
            (Q(excavation__owner=request.user) | Q(excavation__users=request.user)) &
            Q(is_active=True)
        ).distinct()
        serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def sector_detail(request, pk):
    try:
        sector = Sectors.objects.get(pk=pk, is_active=True)
        excavation = sector.excavation
        if excavation.owner != request.user and request.user not in excavation.users.all():
            return Response(
                {"error": "No tienes permiso para acceder a los sectores de esta excavación"},
                status=status.HTTP_403_FORBIDDEN
            )
    except Sectors.DoesNotExist:
        return Response({"error": "Sector no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SectorSerializer(sector)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = SectorSerializer(sector, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sector.is_active = False
        sector.save()
        return Response(
            {"message": "Sector desactivado correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )
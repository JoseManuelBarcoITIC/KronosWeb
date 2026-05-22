import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Excavations, Sectors, StratigraphicUnit
from .serializers import ExcavationSerializer, SectorSerializer, StratigraphicUnitSerializer


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
                serializer.save()  # HiddenField inyecta el owner automáticamente
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as database_error:
            return Response(
                {"error_internal_django": str(database_error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def excavation_detail(request, pk):
    try:
        excavation = Excavations.objects.get(pk=pk, is_active=True)
        if excavation.owner != request.user and request.user not in excavation.users.all():
            return Response({"error": "No tienes permiso para acceder a este yacimiento"}, status=status.HTTP_403_FORBIDDEN)
    except Excavations.DoesNotExist:
        return Response({"error": "Yacimiento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExcavationSerializer(excavation)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        if 'users' in request.data and excavation.owner != request.user:
            return Response(
                {"error": "Solo el administrador/creador del yacimiento puede modificar los miembros del equipo."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ExcavationSerializer(excavation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        excavation.is_active = False
        excavation.save()
        return Response({"message": "Excavación desactivada correctamente"}, status=status.HTTP_204_NO_CONTENT)


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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def stratigraphic_unit_list(request):
    if request.method == 'GET':
        units = StratigraphicUnit.objects.filter(
            (Q(sector__excavation__owner=request.user) | Q(sector__excavation__users=request.user)) &
            Q(is_active=True)
        ).distinct()
        serializer = StratigraphicUnitSerializer(units, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        payload = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'relations' in payload and isinstance(payload['relations'], str):
            try:
                payload['relations'] = json.loads(payload['relations'])
            except ValueError:
                payload['relations'] = []

        serializer = StratigraphicUnitSerializer(data=payload)
        if serializer.is_valid():
            sector = serializer.validated_data['sector']
            if sector.excavation.owner != request.user and request.user not in sector.excavation.users.all():
                return Response(
                    {"error": "No tienes permiso para añadir unidades a este sector"},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def stratigraphic_unit_detail(request, pk):
    try:
        unit = StratigraphicUnit.objects.get(pk=pk, is_active=True)
        excavation = unit.sector.excavation
        if excavation.owner != request.user and request.user not in excavation.users.all():
            return Response(
                {"error": "No tienes permiso para acceder a esta unidad estratigráfica"},
                status=status.HTTP_403_FORBIDDEN
            )
    except StratigraphicUnit.DoesNotExist:
        return Response({"error": "Unidad estratigráfica no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StratigraphicUnitSerializer(unit)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        payload = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'relations' in payload and isinstance(payload['relations'], str):
            try:
                payload['relations'] = json.loads(payload['relations'])
            except ValueError:
                payload['relations'] = []

        serializer = StratigraphicUnitSerializer(unit, data=payload, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        unit.is_active = False
        unit.save()
        return Response(
            {"message": "Unidad estratigráfica desactivada correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )
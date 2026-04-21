from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Excavations
from .serializers import ExcavationSerializer
from django.db.models import Q
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def excavation_list(request):
    user = request.user

    if request.method == 'GET':
        excavations = Excavations.objects.filter(
            Q(owner=user) | Q(users=user)
        ).distinct()

        serializer = ExcavationSerializer(excavations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExcavationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
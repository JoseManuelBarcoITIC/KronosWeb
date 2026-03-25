from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Excavations
from .serializers import ExcavationSerializer

@api_view(['GET', 'POST'])
def excavation(request):
    if request.method == 'GET':
        excavations = Excavations.objects.filter(
            models.Q(owner=request.user) | models.Q(users=request.user)
        ).distinct()
        serializer = ExcavationSerializer(excavations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExcavationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
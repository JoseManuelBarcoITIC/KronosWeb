from rest_framework import serializers
from .models import Excavations

class ExcavationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excavations
        fields = [ 'name', 'owner']
        read_only_fields = ['id']
from rest_framework import serializers
from .models import Excavations

class ExcavationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excavations
        fields = '__all__'

    def create(self, validated_data):
        users = validated_data.pop('users', [])

        excavation = Excavations.objects.create(**validated_data)

        excavation.users.set(users)

        return excavation
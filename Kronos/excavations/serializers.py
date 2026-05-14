from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Excavations, Sectors

# Detecta el modelo de usuario correcto de tu sistema dinámicamente
User = get_user_model()


class SectorSerializer(serializers.ModelSerializer):
    excavation_name = serializers.ReadOnlyField(source='excavation.name')

    class Meta:
        model = Sectors
        fields = ['id', 'name', 'excavation', 'excavation_name']


class ExcavationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(is_active=True),
        required=False
    )

    class Meta:
        model = Excavations
        fields = ['id', 'name', 'users', 'owner', 'is_active', 'estatExcavacio']
        read_only_fields = ['id', 'is_active']

    def validate_users(self, value):
        for user in value:
            if not user.is_active:
                raise serializers.ValidationError(
                    f"El usuario {user.id} no está activo"
                )
        return value

    def create(self, validated_data):
        users = validated_data.pop('users', [])

        excavation = Excavations.objects.create(estatExcavacio='Activa', **validated_data)

        if users:
            excavation.users.set(users)

        return excavation

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.id if instance.owner else None
        return representation
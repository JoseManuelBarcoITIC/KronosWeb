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
    # Usar HiddenField requiere pasar el contexto 'request' (ya lo haces en la vista)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(is_active=True),
        required=False
    )

    class Meta:
        model = Excavations
        # Definimos los campos explícitamente en lugar de '__all__' para evitar atascos de DRF
        fields = ['id', 'name', 'users', 'owner', 'is_active']
        read_only_fields = ['id', 'is_active']

    def validate_users(self, value):
        for user in value:
            if not user.is_active:
                raise serializers.ValidationError(
                    f"El usuario {user.id} no está activo"
                )
        return value

    def create(self, validated_data):
        # Extraemos los IDs de los usuarios asignados
        users = validated_data.pop('users', [])

        # El validated_data ya contiene el 'owner' gracias al HiddenField
        excavation = Excavations.objects.create(**validated_data)

        # Guardamos la relación ManyToMany una vez el yacimiento tiene ID
        if users:
            excavation.users.set(users)

        return excavation

    def to_representation(self, instance):
    git
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.id if instance.owner else None
        return representation
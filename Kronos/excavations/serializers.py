from rest_framework import serializers
from .models import Excavations, Sectors
from users.models import User


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
        fields = '__all__'

    def validate_users(self, value):
        for user in value:
            if not user.is_active:
                raise serializers.ValidationError(
                    f"El usuario {user.id} no está activo"
                )
        return value

    def create(self, validated_data):
        users = validated_data.pop('users', [])

        excavation = Excavations.objects.create(**validated_data)

        if users:
            excavation.users.set(users)

        return excavation
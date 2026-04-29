from rest_framework import serializers
from .models import Excavations
from users.models import User

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

    def validate_users(self, value): # 'value' es el estándar, pero 'users' funciona
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
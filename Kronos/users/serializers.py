from rest_framework import serializers
from .models import User, UserType

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'name']
class UserSerializer(serializers.ModelSerializer):
    type = UserTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=UserType.objects.all(),
        source='type',
        write_only=True
    )
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'surname2', 'email', 'type', 'type_id']
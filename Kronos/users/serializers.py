from .models import UserType
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.hashers import check_password

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    type = UserTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=UserType.objects.all(),
        source='type',
        write_only=True
    )
    class Meta:
        model = User
        fields = ['id', 'name', 'password','surname', 'surname2', 'email', 'type', 'type_id']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name', 'surname']

class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('Correo o contraseña incorrectos')

        if not user.is_active:
            raise serializers.ValidationError('Usuario inactivo')

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'is_staff': user.is_staff,
                'type': user.type.name
            }
        }
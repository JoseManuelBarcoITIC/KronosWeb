from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'surname', 'surname2', 'email', 'is_staff', 'is_superuser']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname', 'is_staff', 'is_superuser']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname', 'surname2', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        is_superuser = validated_data.get('is_superuser', None)

        if is_superuser is not None:
            instance.is_superuser = is_superuser
            instance.is_staff = is_superuser  # Si es Superadmin, también posee rol Staff

        # Seteamos el resto de campos validados
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname', 'surname2', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        is_superuser = validated_data.get('is_superuser', False)

        if is_superuser:
            validated_data['is_staff'] = True

        # Conexión directa y nativa al CustomUserManager del modelo
        user = User.objects.create_user(**validated_data)
        return user


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
                'is_superuser': user.is_superuser
            }
        }
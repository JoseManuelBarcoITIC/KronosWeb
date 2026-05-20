from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Excavations, Sectors, StratigraphicUnit, UERelationship

User = get_user_model()


class SectorSerializer(serializers.ModelSerializer):
    excavation_name = serializers.ReadOnlyField(source='excavation.name')

    class Meta:
        model = Sectors
        fields = ['id', 'name', 'excavation', 'excavation_name']

class UERelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UERelationship
        fields = ['to_ue', 'type_relation']

class ExcavationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(is_active=True),
        required=False
    )

    class Meta:
        model = Excavations
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
        users = validated_data.pop('users', [])
        excavation = Excavations.objects.create(**validated_data)

        if users:
            excavation.users.set(users)

        return excavation

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.id if instance.owner else None
        return representation




class StratigraphicUnitSerializer(serializers.ModelSerializer):
    sector_name = serializers.ReadOnlyField(source='sector.name')
    relations = UERelationshipSerializer(many=True, required=False, source='from_relations')

    class Meta:
        model = StratigraphicUnit
        fields = [
            'id', 'sector', 'sector_name', 'ue_number', 'definition',
            'length', 'width', 'height', 'top_elevation', 'bottom_elevation',
            'sheet_data', 'site_photo', 'relations', 'description', 'is_active'
        ]
        read_only_fields = ['id', 'is_active']

    def create(self, validated_data):
        relations_data = validated_data.pop('from_relations', [])
        unit = StratigraphicUnit.objects.create(**validated_data)

        for relation in relations_data:
            UERelationship.objects.create(
                from_ue=unit,
                to_ue=relation['to_ue'],
                type_relation=relation['type_relation']
            )
        return unit

    def update(self, instance, validated_data):
        relations_data = validated_data.pop('from_relations', None)
        instance = super().update(instance, validated_data)

        if relations_data is not None:
            UERelationship.objects.filter(from_ue=instance).delete()
            for relation in relations_data:
                UERelationship.objects.create(
                    from_ue=instance,
                    to_ue=relation['to_ue'],
                    type_relation=relation['type_relation']
                )
        return instance
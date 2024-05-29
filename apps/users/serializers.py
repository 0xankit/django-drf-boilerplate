from webbrowser import get

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, Designation, Role


class RoleSerializer(serializers.ModelSerializer):
    """ 
    Role Serializer
    """
    class Meta:
        """
        Meta Class For Role Serializer
        """
        model = Role
        fields = ['id', 'name']


class DesignationSerializer(serializers.ModelSerializer):
    """
    Designation Serializer
    """
    class Meta:
        """
        Meta Class For Designation Serializer
        """
        model = Designation
        fields = ['id', 'title']


class UserSerializer(serializers.ModelSerializer):
    """ 
    User Serializer
    """
    roles = RoleSerializer(many=True, read_only=True)
    designation = DesignationSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})

    class Meta:
        """ Meta Class For Custom User"""
        model = CustomUser
        fields = ('id', 'email',
                  'first_name', 'last_name', 'password', 'roles', 'designation')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data['email'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              password=validated_data['password'])
        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', [])
        designation = validated_data.pop('designation', None)

        instance = super().update(instance, validated_data)
        if designation:
            instance.designation = get_object_or_404(
                Designation, id=designation['id'])
        if roles_data:
            instance.roles.clear()
            for role in roles_data:
                _roles = get_object_or_404(Role, id=role['id'])
                instance.roles.add(_roles)
        instance.save()
        return instance


# class LoginResponseSerializer(serializers.Serializer):
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token Obtain Pair Serializer

    Args:
        TokenObtainPairSerializer (TokenObtainPairSerializer): Token Obtain Pair Serializer

    Returns:
        dict: Token Pair
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        if user.designation:
            token['designation'] = user.designation.title
        if user.roles:
            token['roles'] = [role.name for role in user.roles.all()]
        return token

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ManageUserRolesSerializer(serializers.ModelSerializer):
    """
    Manage User Roles Serializer
    """
    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), many=True)

    class Meta:
        """
        Meta Class For Manage User Roles Serializer
        """
        model = CustomUser
        fields = ['id', 'roles']

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', [])

        # instance = super().update(instance, validated_data)
        with transaction.atomic():
            if roles_data:
                instance.roles.clear()
                for role in roles_data:
                    instance.roles.add(role)
            instance.save()
        return instance

    def to_internal_value(self, data):
        if 'roles' in data:
            roles = data.pop('roles')
            try:
                data['roles'] = [get_object_or_404(
                    Role, name=role['name'].upper()).id for role in roles]
            except Http404:
                raise serializers.ValidationError(
                    {'roles': 'Role not found'})
        return super().to_internal_value(data)


class ManageUserDesignation(serializers.ModelSerializer):
    """
    Manage User Designation Serializer
    """
    designation = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(), required=True)

    class Meta:
        """
        Meta Class For Manage User Designation Serializer
        """
        model = CustomUser
        fields = ['id', 'designation']

    def update(self, instance, validated_data):
        designation = validated_data.pop('designation', None)
        if designation:
            instance.designation = designation
            instance.save()
        return instance

    def to_internal_value(self, data):
        if 'designation' in data:
            designation = data.pop('designation')
            try:
                data['designation'] = get_object_or_404(
                    Designation, title=designation['title'].upper()).id
            except Http404:
                raise serializers.ValidationError(
                    {'designation': _('Designation not found')})
        return super().to_internal_value(data)

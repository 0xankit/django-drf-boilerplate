from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('id', 'email',
                  'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data['email'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              password=validated_data['password'])
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.set_password(validated_data.get(
            'password', instance.password))
        instance.save()
        return instance

# login serializer


class LoginRequestSerializer(serializers.Serializer):
    """
    Login Request Serializer

    Args:
        serializers (Serializer): Serializer class
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


# class LoginResponseSerializer(serializers.Serializer):

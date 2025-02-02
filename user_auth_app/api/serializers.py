from rest_framework import serializers
from django.contrib.auth.models import User
from ..validators import CustomUsernameValidator
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    username = serializers.CharField(validators=[CustomUsernameValidator()])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Jetzt wird die E-Mail abgefragt
    password = serializers.CharField(write_only=True, required=True)


class GuestLoginSerializer(serializers.Serializer):
    username = serializers.CharField(default='guest', required=False)

    def create(self, validated_data):
        # Gast-Benutzer anlegen (ohne Passwort)
        username = validated_data.get('username', 'guest')
        user, created = User.objects.get_or_create(username=username)

        # Erstelle oder hole das Token für diesen Benutzer
        token, created = Token.objects.get_or_create(user=user)

        return {
            'token': token.key
        }
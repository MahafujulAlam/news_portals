from django.contrib.auth import authenticate
from rest_framework import serializers

#Lander serializer validation
from .models import (Registration)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

    def create(self, validated_data):

        user = Registration(
                first_name=validated_data['first_name'],
                last_name = validated_data['last_name'],
                mobile_number=validated_data['mobile_number'],
                email=validated_data['email'],

            )

        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    model = Registration
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

        first_name = serializers.CharField(required=True)
        last_name = serializers.CharField()


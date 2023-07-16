from django.contrib.auth import get_user_model
from dj_rest_auth.registration import serializers as dj_rest_auth_registration_serializers
from rest_framework import serializers


UserModel = get_user_model()

class RegisterSerializer(dj_rest_auth_registration_serializers.RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


    def validate_phone_number(self, phone_number: str):
        phone_number_exists: bool = UserModel.objects.filter(phone_number=phone_number).exists()
        if phone_number_exists:
            raise serializers.ValidationError(
                "A user with this phone number already exists", "invalid"
            )
        return phone_number

    def validate_username(self, username):
        pass

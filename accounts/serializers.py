import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def validate_username(value):
    if not re.match(r"^[A-Za-zА-Яа-яЇїЄєІіҐґ0-9]{1,40}$", value):
        raise serializers.ValidationError(
            "User ID must contain only Latin/Ukrainian letters and digits, "
            "without special characters."
        )
    return value


def validate_name(value):
    if not re.match(r"^[A-Za-zА-Яа-яЇїЄєІіҐґ-]{1,50}$", value):
        raise serializers.ValidationError(
            "Only Latin/Ukrainian letters and hyphens are allowed."
        )
    return value


def validate_phone(value):
    if not re.match(r"^\+38 \d{3} \d{3} \d{2} \d{2}$", value):
        raise serializers.ValidationError(
            "Phone number must be in format +38 ХХХ ХХХ ХХ ХХ."
        )
    return value


def validate_password_custom(value):
    if len(value) < 8 or len(value) > 30:
        raise serializers.ValidationError(
            "Password must be between 8 and 30 characters."
        )
    if not re.search(r"[A-Z]", value):
        raise serializers.ValidationError(
            "Password must contain at least one uppercase letter."
        )
    if not re.search(r"[0-9]", value):
        raise serializers.ValidationError(
            "Password must contain at least one digit."
        )
    if not re.search(r"[\W_]", value):
        raise serializers.ValidationError(
            "Password must contain at least one special character."
        )
    return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     min_length=8,
                                     max_length=30)
    password_repeat = serializers.CharField(write_only=True,
                                            min_length=8,
                                            max_length=32)

    class Meta:
        model = User
        fields = ["username",
                  "first_name",
                  "last_name",
                  "email",
                  "phone",
                  "password",
                  "password_repeat"]

    def validate_username(self, value):
        return validate_username(value)

    def validate_first_name(self, value):
        return validate_name(value)

    def validate_last_name(self, value):
        return validate_name(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def validate_password(self, value):
        return validate_password_custom(value)

    def validate(self, data):
        if data["password"] != data["password_repeat"]:
            raise serializers.ValidationError(
                {"password_repeat": "Passwords do not match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password_repeat")  # Убираем, так как не нужно для создания
        user = User(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone=validated_data["phone"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

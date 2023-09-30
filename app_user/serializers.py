from typing import Dict, Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from app_shop.validators import validate_not_blank
from .models import CustomUser


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.

    Настроена проверка пароля.
    Пароль должен быть не короче 8 символов и содержать хотя бы одну цифру и одну букву.

    Настроена проверка имени и фамилии.
    Имя и фамилия не могу быть пустыми строками и состоять только из одних пробелов.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True, validators=[validate_not_blank])
    last_name = serializers.CharField(required=True, validators=[validate_not_blank])

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Проверяет валидность данных сериализатора.
        Возвращает входные данные сериализатора после проверки валидности.

        :param attrs: Входные данные сериализатора.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        """
        Создает новый экземпляр модели CustomUser с переданными данными.
        Устанавливает пароль пользователя.
        Сохраняет пользователя в базе данных.

        :param validated_data: Валидированные данные сериализатора.
        """
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=True
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

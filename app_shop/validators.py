from django.core.exceptions import ValidationError


def validate_not_blank(value: str) -> None:
    """
    Валидатор для проверки, что значение не является пустым или состоящим только из пробелов.

    :param value: Значение для проверки.
    :raises ValidationError: Если значение пусто или состоит только из пробелов.
    """
    if not value.strip():
        raise ValidationError("Это поле не может быть пустым или состоять только из пробелов")

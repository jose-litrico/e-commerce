from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

def validate_positive_integer(value: int, field_name="value"):
    try:
        value = int(value)

        if value <= 0:
            raise ValidationError({field_name: "Debe ser un numero entero mayor a 0"})

        return value
    except (TypeError, ValueError):
        raise ValidationError({field_name: "Debes ser un numero entero valido"})

def get_object_or_validation_error(model, pk: int, field_name="id"):
    try:
        return model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise ValidationError({field_name: f"{model.__name__} no encontrado"})
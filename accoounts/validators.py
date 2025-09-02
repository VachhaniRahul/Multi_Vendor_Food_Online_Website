import os

from django.core.exceptions import ValidationError


def allow_only_images_validators(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    validate_ext = [".png", ".jpg", ".jpeg"]
    if ext.lower() not in validate_ext:
        raise ValidationError(
            "Unsupported file extension. Allowed extension: " + str(validate_ext)
        )

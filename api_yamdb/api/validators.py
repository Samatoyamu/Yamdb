import re

from django.core.exceptions import ValidationError


def validate_regex(value):
    reg = re.compile(r'^[\w.@+-]+')
    if not reg.match(value):
        raise ValidationError('Имя не соответствует регулярному выражению')

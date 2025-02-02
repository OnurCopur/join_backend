from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

@deconstructible
class CustomUsernameValidator(RegexValidator):
    regex = r'^[\w.@+\-\s]+$'
    message = 'Enter a valid username. This value may contain only letters, numbers, spaces, and @/./+/-/_ characters.'
    flags = 0

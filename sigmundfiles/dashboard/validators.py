from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Tu contraseña debe contener al menos 8 caracteres."),
                code='password_too_short',
            )
        if re.match(r'^\d+$', password):
            raise ValidationError(
                _("Tu contraseña no puede ser completamente numérica."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos 8 caracteres y no puede ser completamente numérica."
        )

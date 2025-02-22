import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ..db import CachedManager


class EmailManager(CachedManager):
    natural_key = ['email']

    def get_by_email(self, email: str) -> "UserEmail":
        return self.get_from_cache_by_natural_key(email)


class UserEmail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    objects = EmailManager()

    class Meta:
        verbose_name = _("email")
        verbose_name_plural = _("emails")
        ordering = ['created_at']
        db_table = 'saas_auth_email'

    def __str__(self):
        return self.email

    def natural_key(self):
        return self.email,

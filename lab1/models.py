from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Document(models.Model):
    class DocumentType(models.TextChoices):
        VACATION_REQUEST = 'VR', _('Vacation Request')
        EMPLOYMENT_APPLICATION = 'EA', _('Employment Application')

    name = models.CharField(max_length=255, verbose_name="Document Name")
    doc_type = models.CharField(
        max_length=2,
        choices=DocumentType.choices,
        verbose_name="Document Type"
    )
    body = models.TextField(verbose_name="Document Body")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    signature_date = models.DateTimeField(null=True, blank=True, verbose_name="Signature Date")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self) -> str:
        return self.name or '-'

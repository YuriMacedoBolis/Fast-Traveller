from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField("e-mail", max_length=254, unique=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "usuarios"
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.username

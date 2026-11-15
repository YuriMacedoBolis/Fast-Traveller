from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Usuário do fast Traveller.

    Estende o AbstractUser do Django apenas para tornar o e-mail obrigatório e
    único, conforme o documento de modelo de dados (tabela `usuarios`) e o
    UC01 - Cadastrar e Autenticar Usuário.
    """

    email = models.EmailField("e-mail", max_length=254, unique=True)

    # username continua sendo o USERNAME_FIELD; o e-mail passa a ser exigido
    # tambem na criacao de superusuarios.
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "usuarios"
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.username

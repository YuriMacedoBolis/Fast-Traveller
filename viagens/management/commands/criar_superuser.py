import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria o superusuario definido em DJANGO_SUPERUSER_* se ainda nao existir."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        senha = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not (username and email and senha):
            self.stdout.write("Variaveis DJANGO_SUPERUSER_* nao definidas.")
            return

        Usuario = get_user_model()
        if Usuario.objects.filter(username=username).exists():
            self.stdout.write(f"Superusuario '{username}' ja existe.")
            return

        Usuario.objects.create_superuser(username=username, email=email, password=senha)
        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' criado."))

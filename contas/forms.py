from django import forms
from django.contrib.auth.forms import UserCreationForm

from contas.models import Usuario


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="E-mail", max_length=254)

    class Meta:
        model = Usuario
        fields = ["first_name", "username", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com esse e-mail.")
        return email

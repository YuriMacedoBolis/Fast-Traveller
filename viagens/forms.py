from datetime import date

from django import forms

from viagens.models import Viagem


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = ["destino", "data_inicio", "duracao_dias", "orcamento_total"]
        widgets = {
            "destino": forms.TextInput(
                attrs={"placeholder": "Ex.: São Paulo, SP", "autofocus": True}
            ),
            "data_inicio": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "duracao_dias": forms.NumberInput(attrs={"min": 1, "max": 60}),
            "orcamento_total": forms.NumberInput(
                attrs={"min": "0.01", "step": "0.01", "placeholder": "1500.00"}
            ),
        }

    def clean_destino(self):
        destino = self.cleaned_data["destino"].strip()
        if len(destino) < 3:
            raise forms.ValidationError("Informe um destino com pelo menos 3 caracteres.")
        return destino

    def clean_data_inicio(self):
        data_inicio = self.cleaned_data["data_inicio"]
        if data_inicio < date.today():
            raise forms.ValidationError("A data de início não pode estar no passado.")
        return data_inicio

    def clean_orcamento_total(self):
        orcamento = self.cleaned_data["orcamento_total"]
        if orcamento <= 0:
            raise forms.ValidationError("O orçamento deve ser maior que zero.")
        return orcamento


class BuscaViagemForm(forms.Form):
    destino = forms.CharField(
        required=False,
        label="Destino",
        widget=forms.TextInput(attrs={"placeholder": "Buscar por destino"}),
    )
    data_inicio_apos = forms.DateField(
        required=False,
        label="A partir de",
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
    )
    orcamento_min = forms.DecimalField(
        required=False,
        label="Orçamento mínimo",
        min_value=0,
        widget=forms.NumberInput(attrs={"step": "0.01", "placeholder": "0,00"}),
    )

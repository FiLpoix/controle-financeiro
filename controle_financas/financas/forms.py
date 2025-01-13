from django import forms
from .models import Transacao, Categoria

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'tipo', 'valor', 'data', 'categoria']
from django import forms
from .models import PAYMENT_OPTION_CHOICES, DONATE_TYPE_CHOICES

class DonateForm(forms.Form):
    donor_name = forms.CharField(label='Nome', max_length=100)
    donor_email = forms.EmailField(label='Email')
    donate_Type = forms.CharField(
        label='Tipo da doação',
        widget=forms.Select(choices=DONATE_TYPE_CHOICES)
    )
    payment_option = forms.CharField(
        label='Forma de Pagamento',
        widget=forms.Select(choices=PAYMENT_OPTION_CHOICES)
    )
    amount = forms.FloatField(label='Valor (R$)')
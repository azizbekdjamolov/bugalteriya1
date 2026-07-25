from django import forms
from .models import Party, Debt


class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['type', 'name', 'phone', 'address', 'default_currency', 'notes']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'default_currency': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['party', 'direction', 'amount', 'currency', 'paid_amount', 'due_date', 'description']
        widgets = {
            'party': forms.Select(attrs={'class': 'form-select'}),
            'direction': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DebtFilterForm(forms.Form):
    direction = forms.ChoiceField(required=False, choices=[('', 'Barchasi')] + list(Debt.Direction.choices),
                                   widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(required=False, choices=[('', 'Barchasi')] + list(Debt.Status.choices),
                                widget=forms.Select(attrs={'class': 'form-select'}))
    currency = forms.CharField(required=False, widget=forms.Select(
        choices=[('', 'Barchasi')] + list(Debt._meta.get_field('currency').choices),
        attrs={'class': 'form-select'}))
    q = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Kontragent nomi bo\'yicha qidirish'}))

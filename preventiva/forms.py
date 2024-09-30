from django import forms
from django.core.exceptions import ValidationError


class PreventivaForm(forms.Form):
    data_inicial = forms.DateField(
        label="Data Inicial",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        help_text="Data inicial das preventivas")
    data_final = forms.DateField(
        label="Data Final",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"],
        help_text="Data Final das preventivas")

    def clean(self):
        cleaned_data = super(PreventivaForm, self).clean()
        data_inicial = cleaned_data.get("data_inicial")
        data_final = cleaned_data.get("data_final")

        if data_inicial > data_final:
            raise ValidationError("Data inicial não pode ser depois de data final!")

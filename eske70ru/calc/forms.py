from django import forms


class OhmLawForm(forms.Form):
    voltage = forms.FloatField(
        required=False,
        label="Напряжение (В)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    current = forms.FloatField(
        required=False,
        label="Сила тока (А)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    resistance = forms.FloatField(
        required=False,
        label="Сопротивление (Ом)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )

    def clean(self):
        cleaned_data = super().clean()
        voltage = cleaned_data.get('voltage')
        current = cleaned_data.get('current')
        resistance = cleaned_data.get('resistance')

        # Проверяем, что заполнено ровно 2 поля из 3
        filled_fields = sum(1 for field in [voltage, current, resistance] if field is not None)

        if filled_fields != 2:
            raise forms.ValidationError("Необходимо заполнить ровно два поля из трех!")

        return cleaned_data
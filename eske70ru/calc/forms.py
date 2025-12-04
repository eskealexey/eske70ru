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
#
# class VoltageDividerForm(forms.Form):
#     voltage_input = forms.FloatField(
#         required=False,
#         label="Напряжение (В)",
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
#     )
#     resistance_1 = forms.FloatField(
#         required=False,
#         label="Сопротивление R1 (Ом)",
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Например: 10.0'})
#     )
#     resistance_2 = forms.FloatField(
#         required=False,
#         label="Сопротивление R2 (Ом)",
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Например: 10.0'})
#     )
#     resistance_load = forms.FloatField(
#         required=False,
#         label="Сопротивление нагрузки (Ом)",
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Например: 10.0'}))
#
#     def clean(self):
#         cleaned_data = super().clean()
#         for field_name, value in cleaned_data.items():
#             if value is not None and value < 0:
#                 self.add_error(field_name, "Значение не может быть отрицательным.")
#         return cleaned_data
#
#
# /eske70ru/calc/forms.py
# from django import forms
#
# class VoltageDividerForm(forms.Form):
#     voltage_input = forms.FloatField(
#         required=False,
#         label="Напряжение питания (В)",
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.1',
#             'placeholder': 'Например: 5.0'
#         })
#     )
#     resistance_1 = forms.FloatField(
#         required=False,
#         label="Сопротивление R1 (Ом)",
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.1',
#             'placeholder': 'Например: 1000.0'
#         })
#     )
#     resistance_2 = forms.FloatField(
#         required=False,
#         label="Сопротивление R2 (Ом)",
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.1',
#             'placeholder': 'Например: 1000.0'
#         })
#     )
#     resistance_load = forms.FloatField(
#         required=False,
#         label="Сопротивление нагрузки (Ом)",
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'step': '0.1',
#             'placeholder': 'Например: 5000.0'
#         })
#     )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         for field_name, value in cleaned_data.items():
#             if value is not None and value < 0:
#                 self.add_error(field_name, "Значение не может быть отрицательным.")
#         return cleaned_data

# /eske70ru/calc/forms.py
from django import forms

class VoltageDividerForm(forms.Form):
    # Основные параметры
    voltage_input = forms.FloatField(
        required=False,
        label="Напряжение питания, В",
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'Например: 5.0'
        })
    )
    voltage_output = forms.FloatField(
        required=False,
        label="Желаемое выходное напряжение, В",
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'Например: 3.3'
        })
    )
    resistance_1 = forms.FloatField(
        required=False,
        label="Сопротивление R1, Ом",
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'Известно или рассчитать'
        })
    )
    resistance_2 = forms.FloatField(
        required=False,
        label="Сопротивление R2, Ом",
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'Известно или рассчитать'
        })
    )
    resistance_load = forms.FloatField(
        required=False,
        label="Сопротивление нагрузки, Ом",
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'Опционально'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        v_in = cleaned_data.get('voltage_input')
        v_out = cleaned_data.get('voltage_output')
        r1 = cleaned_data.get('resistance_1')
        r2 = cleaned_data.get('resistance_2')
        r_load = cleaned_data.get('resistance_load')

        # Проверка на отрицательные значения
        for field_name, value in cleaned_data.items():
            if value is not None and value < 0:
                self.add_error(field_name, "Значение не может быть отрицательным.")

        # Логическая проверка
        if v_in and v_out and v_out >= v_in:
            self.add_error('voltage_output', "V_out должно быть меньше V_in.")

        if v_in and v_out and v_out < 0:
            self.add_error('voltage_output', "V_out не может быть отрицательным.")

        return cleaned_data

from django import forms
from .models import Program

# class ProgramForm(forms.ModelForm):
#     description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
#
#     class Meta:
#         model = Program
#         fields = ['mame', 'short_description', 'description']
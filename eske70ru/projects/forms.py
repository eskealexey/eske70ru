from django import forms
from .models import Comment

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']
#         widgets = {
#             'text': forms.Textarea(attrs={'rows': 3}),
#         }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']  # Добавляем поле parent
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите ваш комментарий...'
            }),
            'parent': forms.HiddenInput()  # Скрытое поле для parent_id
        }
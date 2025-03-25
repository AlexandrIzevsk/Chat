from django import forms
from .models import Customer, Message


class MessageForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}), required=True)

    class Meta:
        model = Message
        fields = ['text',]


class CustomerForm(forms.ModelForm):
    nickname = forms.CharField(label="Ник", max_length=30)
    avatar = forms.ImageField(label="Аватар", required=False)

    class Meta:
        model = Customer
        fields = [
            'nickname',
            'avatar',
        ]

        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Tool
from captcha.fields import CaptchaField

class OperationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keeper'].empty_label = 'Владелец не выбран'

    class Meta:
        model = Tool
        fields = ('keeper', 'quantity')
        # Пример пользовательского оформления полей
        # widgets = {
        #     'keeper': forms.Select(attrs={'class':'form-select-keeper'})
        # }
        # Пример пользовательского валидатора

    def clean_keeper(self):
        keeper = self.cleaned_data['keeper']
        if len(str(keeper)) > 200:
            raise ValidationError('Длина первышает 200 символов')
        return keeper


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    username = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'row': 10}))
    captcha = CaptchaField()
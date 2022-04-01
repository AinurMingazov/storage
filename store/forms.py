from django import forms
from django.core.exceptions import ValidationError

from .models import Tool


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

class RegisterUserForm(UserCreationForm)
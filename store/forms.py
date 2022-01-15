from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Operation, Tool


class OperationForm(forms.ModelForm):

    # def clean_keeper(self):
    #     tool = get_object_or_404(Tool, id=id)
    #     data = self.cleaned_data['keeper']
    #
    #     if data == tool.keeper:
    #         raise ValidationError('Тот же владелец')
    #     return data
    #
    # def clean_quantity(self):
    #     tool = get_object_or_404(Tool, id=id)
    #     data = self.cleaned_data['quantity']
    #
    #     if data > tool.quantity:
    #         raise ValidationError('Недостаточно инструмента')
    #     return data

    class Meta:
        model = Tool
        fields = ('keeper', 'quantity')

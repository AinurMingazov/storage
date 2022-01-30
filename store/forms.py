from django import forms

from .models import Tool


class OperationForm(forms.ModelForm):

    class Meta:
        model = Tool
        fields = ('keeper', 'quantity')

from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Operation, Tool


class OperationForm(forms.ModelForm):

    class Meta:
        model = Tool
        fields = ('keeper', 'quantity')

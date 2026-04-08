from django import forms

from .models import FabricStock


class FabricStockForm(forms.ModelForm):
    class Meta:
        model = FabricStock
        fields = ["fabric_type", "meter_available", "meter_used"]


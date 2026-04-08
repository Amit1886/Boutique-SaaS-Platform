from django import forms

from .models import Order, Product, TryOnRequest


class TryOnUploadForm(forms.ModelForm):
    class Meta:
        model = TryOnRequest
        fields = ["user_image", "bust_size", "waist_size", "height"]
        widgets = {
            "bust_size": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "waist_size": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "height": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }


class OrderConfirmForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(), empty_label=None, required=True
    )

    class Meta:
        model = Order
        fields = ["product"]


from django import forms

from .models import VendorProfile


class VendorSettingsForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ["business_name", "theme_color", "upi_id"]


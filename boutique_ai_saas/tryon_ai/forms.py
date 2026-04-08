from django import forms


class VirtualUploadForm(forms.Form):
    photo = forms.ImageField()
    tryon_type = forms.ChoiceField(choices=[("2D", "2D"), ("3D", "3D"), ("AR", "AR")], initial="2D")
    manual_bust = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    manual_waist = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    manual_height = forms.DecimalField(required=False, max_digits=6, decimal_places=2)


class OrderConfirmForm(forms.Form):
    product_id = forms.IntegerField()


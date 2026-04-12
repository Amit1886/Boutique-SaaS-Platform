from django import forms


class VirtualUploadForm(forms.Form):
    photo = forms.ImageField()
    tryon_type = forms.ChoiceField(choices=[("2D", "2D"), ("3D", "3D"), ("AR", "AR")], initial="2D")
    manual_bust = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    manual_waist = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    manual_height = forms.DecimalField(required=False, max_digits=6, decimal_places=2)


class OrderConfirmForm(forms.Form):
    product_id = forms.IntegerField()


class VideoTryOnForm(forms.Form):
    video = forms.FileField()
    template_id = forms.IntegerField(required=False)


class BlouseDesignerForm(forms.Form):
    neck = forms.ChoiceField(
        choices=[("round", "Round"), ("v-neck", "V-neck"), ("sweetheart", "Sweetheart"), ("square", "Square")],
        initial="round",
    )
    sleeve = forms.ChoiceField(
        choices=[("sleeveless", "Sleeveless"), ("cap", "Cap"), ("short", "Short"), ("long", "Long")],
        initial="short",
    )
    back = forms.ChoiceField(
        choices=[("u-back", "U-back"), ("deep-back", "Deep back"), ("keyhole", "Keyhole")],
        initial="u-back",
    )
    pattern = forms.ChoiceField(
        choices=[("solid", "Solid"), ("floral", "Floral"), ("geometric", "Geometric")],
        initial="solid",
    )
    border = forms.ChoiceField(
        choices=[("none", "None"), ("lace", "Lace"), ("gold", "Gold"), ("mirror", "Mirror")],
        initial="none",
        required=False,
    )
    color = forms.CharField(initial="#db2777")


class BlueprintForm(forms.Form):
    blueprint_type = forms.ChoiceField(
        choices=[("blouse", "Blouse cutting sheet"), ("fall_pico", "Saree fall/pico sheet")],
        initial="blouse",
    )
    bust_in = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    waist_in = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    hips_in = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    shoulder_in = forms.DecimalField(required=False, max_digits=6, decimal_places=2)

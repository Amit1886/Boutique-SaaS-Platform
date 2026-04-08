from django import forms


class POSForm(forms.Form):
    name = forms.CharField(max_length=120)
    phone = forms.CharField(max_length=30, required=False)
    item_list_json = forms.CharField(
        widget=forms.Textarea,
        help_text='JSON list, e.g. [{"name":"Saree","qty":1,"price":2499}]',
    )


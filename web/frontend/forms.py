from django import forms

class login_form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

class create_account_form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

class create_listing_form(forms.Form):
    device_type = forms.CharField(max_length=50)
    device_model = forms.CharField(max_length=50)
    manufacturer = forms.CharField(max_length=50)
    price = forms.FloatField()
    rental_details = forms.CharField(max_length=400)

class search_form(forms.Form):
    query = forms.CharField(max_length=50)

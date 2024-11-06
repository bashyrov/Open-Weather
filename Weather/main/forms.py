from django import forms


class CitySearchForm(forms.Form):
    city_name = forms.CharField(label="City Name", max_length=100, required=True)


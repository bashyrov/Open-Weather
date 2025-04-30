from django import forms


class CitySearchForm(forms.Form):
    city_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'city',
            'placeholder': 'City',}),
        label="City Name",
        max_length=50,
        required=True,
    )

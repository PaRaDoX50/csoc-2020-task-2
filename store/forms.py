from django import forms

class RatingForm(forms.Form):
    rating = forms.FloatField(max_value=10, min_value=0,)
    class Meta:
        fields=('rating')
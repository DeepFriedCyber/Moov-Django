# property_search/forms.py

from django import forms

class NaturalLanguageSearchForm(forms.Form):
    """Form for natural language property search"""
    query = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Describe your ideal property...',
                'aria-label': 'Property search',
            }
        )
    )
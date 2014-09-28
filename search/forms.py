from django import forms

# Search Form 

# ON SUBMIT REENTER ALL SEARCH TERMS INTO TERM AND SEARCH ON WHOLE LIST

class SearchForm(forms.Form):
	query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter your search terms'}), min_length=1)

from django import forms


class BookingForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'firstName',
        'placeholder': 'First name',
        'aria-label': 'First name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'lastName',
        'placeholder': 'Last name',
        'aria-label': 'Last name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'placeholder': 'Email',
        'aria-label': 'email'
    }))
    title = forms.ChoiceField(choices=[
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss')
    ], widget=forms.Select(attrs={
        'class': 'form-select',
        'id': 'selectTitle'
    }))
    
class BookingLookupForm(forms.Form):
    reference = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class':       'form-control',
            'id':          'lookupReference',
            'placeholder': 'Enter your booking reference',
            'aria-label':  'Reference'
        })
    )
    
    
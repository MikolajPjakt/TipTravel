from django import forms
from .models import Trip
from django.utils.translation import gettext_lazy as _

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'purpose', 'start_date', 'end_date', 'notes']
        widgets = {
            'destination': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': _('Np. Paryż, Francja')
            }),
            'purpose': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-input',
                'placeholder': _('Dodatkowe informacje o podróży...')
            }),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_('Data rozpoczęcia nie może być późniejsza niż data zakończenia.'))
        
        return cleaned_data 
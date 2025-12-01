from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('cover_letter',)
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 6,
                'class': 'form-control',
                'placeholder': 'Write your cover letter here...'
            }),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('status', 'notes')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }









from django import forms
from .models import Job


class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'company_name', 'description', 'requirements', 
                  'location', 'salary_min', 'salary_max', 'job_type', 
                  'experience_level', 'skills_required', 'is_remote', 'deadline')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 6}),
            'skills_required': forms.TextInput(attrs={'placeholder': 'e.g., Python, Django, JavaScript, React'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class JobSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search jobs...'
    }))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Location'
    }))
    job_type = forms.ChoiceField(required=False, choices=[('', 'All Types')] + Job.JOB_TYPE_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    experience_level = forms.ChoiceField(required=False, 
                                        choices=[('', 'All Levels')] + Job.EXPERIENCE_LEVEL_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control'}))








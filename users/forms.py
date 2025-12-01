from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, HRProfile



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_hr = forms.BooleanField(required=False, label="Register as HR/Recruiter")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_hr', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Example: custom help text for username only
        self.fields['username'].help_text = ''
        

    # Remove default password help text
        
        self.fields['password1'].help_text = '~Your password can’t be a commonly used password.\n' '~Your password must contain at least 8 characters and can’t be entirely numeric.\n' '~Your password can’t be too similar to your other personal information.'
        self.fields['password2'].help_text = '~Your passwords should match for validation' 
        self.fields['is_hr'].widget.attrs.update({'class': 'custom-checkbox'})


    # Apply a CSS class to all fields so their help text renders smaller
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'small-help'})


    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data['is_hr']:
            user.is_hr = True
            user.is_job_seeker = False
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'email', 'phone', 'bio', 'skills', 
                  'experience_years', 'education', 'location', 
                  'resume', 'profile_picture')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.TextInput(attrs={'placeholder': 'e.g., Python, Django, JavaScript'}),
        }


class HRProfileForm(forms.ModelForm):
    class Meta:
        model = HRProfile
        fields = ('company_name', 'email', 'phone', 'company_description', 
                  'website', 'location')
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }









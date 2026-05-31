from django import forms
from django.contrib.auth.models import User
from .models import * 

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'})


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'phone',
            'branch',
            'tenth_percentage',
            'tweleve_percentage',
            'cgpa',
            'resume'
        ]


class CompanyForm(forms.ModelForm):
    drive_date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Company
        fields = [
            'company_name',
            'job_role',
            'ctc',
            'drive_notice',
            'description',
            'eligibility_cgpa',
            'allowed_branches',
            'drive_date',
            'deadline',
            'image',
        ]
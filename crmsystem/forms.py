from django import forms
from django.contrib.auth import password_validation
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name', 'surname', 'title', 'date_of_birth', 'marks'
        ]


class RegistrationForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match.")
    }

    user_name = forms.CharField(
        label='User name',
        max_length=50,
        help_text='This will be used as Login Name'
    )
    first_name = forms.CharField(
        label='First name',
        max_length=100
    )
    last_name = forms.CharField(
        label='Last name',
        max_length=100
    )
    email = forms.EmailField(
        help_text='Must be in format \'name@server.ext\''
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(),
        help_text=''
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )
    roles = forms.ChoiceField(
        label='Choose role',
        choices=[('cus_ser', 'Customer service'), ('com_owner', 'Company owner')],
        required=True
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if (password1 and password2 and password1 != password2):
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

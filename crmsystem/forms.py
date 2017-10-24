from django import forms
from django.contrib.auth import password_validation
from .models import *


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name', 'surname', 'title', 'date_of_birth', 'marks'
        ]


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = [
            'designer_name', 'designer_surname', 'name_of_mark'
        ]


class ClothForm(forms.ModelForm):
    class Meta:
        model = Cloth
        fields = [
            'name', 'description', 'color', 'size', 'cost_of_piece', 'mark'
        ]


class ContractForm(forms.ModelForm):
    account_iban_number = forms.RegexField(
        label='IBAN číslo účtu',
        max_length=40,
        regex=r'^[A-Z]{2,2}[0-9A-Z]{16,30}$',
    )

    class Meta:
        model = Contract
        fields = [
            'city', 'street_number', 'street_name',
            'account_iban_number',
            'employee', 'customer', 'clothes'
        ]


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'customer', 'description', 'employee'
        ]


class Legal_personForm(forms.ModelForm):
    ico = forms.RegexField(
        label='ICO',
        max_length=8,
        regex=r'(^[0-9]{6,6}$)|(^[0-9]{8,8}$)',
    )
    class Meta:
        model = Legal_person
        fields = [
            'ico', 'name',
        ]
        labels = {
            'name': 'Meno',
        }


class CustomerForm(forms.Form):
    error_messages = {
        'email_exist': ("This email address already exist")
    }

    first_name = forms.CharField(
        label='Meno',
        max_length=150
    )
    last_name = forms.CharField(
        label='Priezvisko',
        max_length=150
    )
    email = forms.EmailField(
        help_text='Must be in format \'name@server.ext\''
    )
    telephone_number = forms.RegexField(
        label='Telefónne číslo',
        max_length=50,
        regex=r'^(\+|00)([0-9,-]+) ([0-9,-]{1,})$',
        help_text='Formát čísla (+/00)country_code number',
    )
    date_of_birth = forms.DateField(
        label='Dátum narodenia',
        input_formats=[
            '%m.%d.%y',
            '%m.%d.%Y',
            '%m-%d-%y',
            '%m-%d-%Y',
        ],
        help_text='Podporovaný formár: mm.dd.yy, mm.dd.yyyy, mm-dd-yy, mm-dd-yyyy'
    )
    city_name = forms.CharField(
        label='Mesto'
    )
    street_name = forms.CharField(
        label='Ulica'
    )
    street_number = forms.IntegerField(
        label='Číslo ulice',
        min_value=0,
    )

    def clean_email(self):
        my_email = self.cleaned_data.get('email')
        if (Customer.objects.filter(email=my_email)):
            raise forms.ValidationError(
                self.error_messages['email_exist'],
                code='email_exist',
            )
        return my_email


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

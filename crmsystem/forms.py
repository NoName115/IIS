from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms

from .models import *


class EmployeeForm(forms.ModelForm):
    error_messages = {
        'username_exists': ("Toto užívateľske meno už existuje")
    }

    class Meta:
        model = Employee
        fields = [
            'username', 'name', 'surname',
            'title', 'date_of_birth',
        ]
        labels = {
            'username': 'Login',
            'name': 'Meno',
            'surname': 'Priezvisko',
            'title': 'Titul',
            'date_of_birth': 'Datum narodenia',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            new_user = User.objects.get(username=username)
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )
        except User.DoesNotExist:
            return username


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = [
            'designer_name', 'designer_surname', 'name_of_mark'
        ]
        labels = {
            'designer_name': 'Meno dizajnéra',
            'designer_surname': 'Priezvisko dizajnéra',
            'name_of_mark': 'Názov značky' 
        }



class ClothForm(forms.ModelForm):
    cost_of_piece = forms.DecimalField(
        label='Cena za kus',
        decimal_places=2,
        max_digits=12,
        min_value=0.00,
    )
    class Meta:
        model = Cloth
        exclude = ('mark',)
        labels = {
            'name': 'Názov',
            'description': 'Popis',
            'color': 'Farba' ,
            'size': 'Veľkosť',
        }


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
            'customer',
        ]


class ContainForm(forms.ModelForm):
    class Meta:
        model = Contain
        fields = [
            'num_of_pieces', 'cloth',
        ]
        labels = {
            'num_of_pieces': 'Počet kusov',
            'cloth': 'Oblečenie',
        }


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'customer', 'description',
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
            'ico', 'company_name',
        ]
        labels = {
            'company_name': 'Meno firmy',
        }


class CustomerForm(forms.ModelForm):
    '''
    error_messages = {
        'email_exist': ("This email address already exist")
    }
    '''

    name = forms.CharField(
        label='Meno',
        max_length=150
    )
    surname = forms.CharField(
        label='Priezvisko',
        max_length=150
    )
    email = forms.EmailField(
        help_text='Must be in format \'name@server.ext\''
    )
    telephone_number = forms.RegexField(
        label='Telefónne číslo',
        max_length=50,
        regex=r'^(\+|00)([0-9,\-]+) ([0-9,\-, ]{1,})$',
        help_text='Formát čísla (+/00)country_code number',
    )
    '''
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
    '''
    street_number = forms.IntegerField(
        label='Číslo ulice',
        min_value=0,
    )

    '''
    def clean_email(self):
        my_email = self.cleaned_data.get('email')
        if (Customer.objects.filter(email=my_email)):
            raise forms.ValidationError(
                self.error_messages['email_exist'],
                code='email_exist',
            )
        return my_email
    '''

    class Meta:
        model = Customer
        fields = [
            'email', 'name', 'surname', 'city', 'street_number',
            'street_name', 'telephone_number', 'employee'
        ]
        labels = {
            'city': 'Mesto',
            'street_name': 'Ulica',
        }


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

from django import forms
from django.core.exceptions import ValidationError

from . import models
from django.core.validators import RegexValidator


class LowerCase(forms.CharField):
    def to_python(self, value):
        return value.lower()


class UpperCase(forms.CharField):
    def to_python(self, value):
        return value.upper()


def custom_validator(value):
    valid_formats = ['png', 'jpeg', 'jpg']
    if not any([True if value.name.endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} is not a valid image format')
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 3 MiB.')


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label='First name', min_length=3, max_length=50,
        validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$', message='Only letters allowed')],
        error_messages={'required': 'First name cannot be empty!'},
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'style': 'font-size: 13px; text-transform:capitalize'}))

    last_name = forms.CharField(label='Last name', min_length=3, max_length=50,
                                validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$', message='Only letters allowed')],
                                widget=forms.TextInput(attrs={'placeholder': 'Last name',
                                                              'style': 'font-size: 13px; text-transform:capitalize'
                                                              }))

    email = LowerCase(label='Email address', min_length=6, max_length=128,
                      validators=[RegexValidator(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',
                                                 message='Please enter valid email')],
                      error_messages={'required': 'Email address cannot be empty'},
                      widget=forms.TextInput(attrs={'placeholder': 'Email address',
                                                    'style': 'font-size: 13px; text-transform:lowercase'}))

    age = forms.CharField(label='Age', min_length=1, max_length=3,
                          validators=[RegexValidator(r'^[0-9]*$', message='Only digits allowed')],
                          error_messages={'required': 'Age field cannot be empty!'},
                          widget=forms.TextInput(attrs={'placeholder': 'Age',
                                                        'style': 'font-size: 13px;'}))

    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'}))

    phone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone', 'data-mask': '(00) 00-00-00',
               'style': 'font-size: 13px; text-transform:capitalize'}))

    GENDER = [('M', 'Male'), ('F', 'Female')]

    gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=GENDER))

    is_donor = forms.BooleanField(label='Register as donor?', required=False, widget=forms.CheckboxInput(
        # attrs={'class': 'custom-control-input'}
    ))

    avatar = forms.FileField(label='Select profile image',
                             required=False,
                             validators=[custom_validator],

                             )

    class Meta:
        model = models.Account
        exclude = [' is_admin', 'is_active', 'is_staff', 'is_superuser']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if models.Account.objects.filter(email=email).exists():
            raise forms.ValidationError('Denied! ' + f'"{email}"' + ' is already registered')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password and password2 and password != password2:
            raise ValidationError("Passwords not match")
        return password2


class LoginForm(forms.Form):

    email = LowerCase(label='Email address', min_length=6, max_length=128,
                      validators=[RegexValidator(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',
                                                 message='Please enter valid email')],
                      error_messages={'required': 'Email address cannot be empty'},
                      widget=forms.TextInput(attrs={'placeholder': 'Email address',
                                                    'style': 'font-size: 13px; text-transform:lowercase'}))

    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'style': 'font-size: 13px;'}))


class DonorForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = ['blood_group', 'email', 'phone', 'avatar', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

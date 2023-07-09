from django import forms
from django.core.validators import RegexValidator

from blood import models


class RequestForm(forms.ModelForm):
    amount = forms.CharField(label='Amount', min_length=1, max_length=3,
                             validators=[RegexValidator(r'^[0-9]*$', message='Only digits allowed')],
                             error_messages={'required': 'Amount field cannot be empty!'},
                             widget=forms.TextInput(attrs={'placeholder': 'Amount',
                                                           'style': 'font-size: 13px;'}))

    reason = forms.CharField(label='Reason', min_length=16, max_length=500,
                             error_messages={'required': 'Reason field cannot be empty!'},
                             widget=forms.TextInput(attrs={'placeholder': 'Reason',
                                                           'style': 'font-size: 13px;'}))

    patient_name = forms.CharField(required=False)
    patient_age = forms.CharField(required=False)
    blood_group = forms.CharField(required=False)

    class Meta:
        model = models.BloodRequest
        fields = ['reason', 'amount', 'patient_name', 'patient_age', 'blood_group']


class DonateForm(forms.ModelForm):
    amount = forms.CharField(label='Amount', min_length=1, max_length=3,
                             validators=[RegexValidator(r'^[0-9]*$', message='Only digits allowed')],
                             error_messages={'required': 'Amount field cannot be empty!'},
                             widget=forms.TextInput(attrs={'placeholder': 'Amount',
                                                           'style': 'font-size: 13px;'}))

    donor_name = forms.CharField(required=False)
    donor_age = forms.CharField(required=False)
    blood_group = forms.CharField(required=False)
    disease = forms.CharField(label='Disease', required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Disease',
                                                            'style': 'font-size: 13px;'}))

    class Meta:
        model = models.BloodDonate
        fields = ['amount', 'donor_name', 'donor_age', 'blood_group', 'disease']


class BloodForm(forms.ModelForm):
    amount = forms.CharField(label='Amount', min_length=1, max_length=3,
                             validators=[RegexValidator(r'^[0-9]*$', message='Only digits allowed')],
                             error_messages={'required': 'Amount field cannot be empty!'},
                             widget=forms.TextInput(attrs={'placeholder': 'Amount',
                                                           'style': 'font-size: 13px;'}))

    class Meta:
        model = models.BloodStock
        fields = ['blood_group', 'amount']

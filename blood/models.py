from django.db import models

from user.models import Account


BLOOD_GROUP = (
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
)


class BloodStock(models.Model):
    blood_group = models.CharField(choices=BLOOD_GROUP, max_length=3)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.blood_group


class BloodRequest(models.Model):
    request_by_patient = models.ForeignKey(Account, null=True, on_delete=models.CASCADE, related_name='accounts')
    patient_name = models.CharField(max_length=30)
    patient_age = models.PositiveIntegerField()
    reason = models.CharField(max_length=500)
    blood_group = models.CharField(max_length=10)
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.blood_group


class BloodDonate(models.Model):
    donor = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    disease = models.CharField(max_length=100, default="Nothing")
    donor_age = models.PositiveIntegerField()
    donor_name = models.CharField(max_length=30, null=True)
    blood_group = models.CharField(max_length=10)
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.donor

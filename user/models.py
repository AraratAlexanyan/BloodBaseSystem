from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from multiselectfield import MultiSelectField


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


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

OTHERS = (
    ('smoker', 'I`am smoker'),
    ('drug', 'I`am use drug'),
    ('drink', 'I`am use alcohol'),
)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True, unique=True)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, default='default.png')
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6)
    is_donor = models.BooleanField(default=False, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    others = MultiSelectField(choices=OTHERS, default='', max_length=32 * 2, blank=True, null=True)
    blood_group = models.CharField(choices=BLOOD_GROUP, max_length=4)
    disease = models.CharField(max_length=100, null=True, blank=True, default=None)
    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # Capitalize (f-name & l-name)

    def clean(self):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

    # Concatenate F-name and L-name (admin Table)

    def name(self):
        return "%s %s" % (self.first_name, self.last_name)




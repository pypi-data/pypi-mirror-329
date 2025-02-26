'''
REFERENCES:

https://github.com/django/django/blob/5a1cae3a5675c5733daf5949759476d65aa0e636/django/contrib/auth/models.py#L471C1-L475C6
'''

# import zoneinfo
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models
from djinntoux.abstract.ab_mod import UUIDpk7
from timezone_field import TimeZoneField


class User(UUIDpk7, AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    surname = models.CharField(blank=True, max_length=150)
    given_names = models.CharField(blank=True, max_length=150)
    surname_first = models.BooleanField(default=False)

    timezone = TimeZoneField(default='America/New_York')

    # override verbose name in admin change list
    # do I need to make a new migration?
    is_staff = models.BooleanField(verbose_name='Staff', default=False,
        help_text='Designates whether the user can log into this admin site.')

    # override verbose name in admin change list
    # do I need to make a new migration?
    is_superuser = models.BooleanField(verbose_name='Super', default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.')

    class Meta:
        ordering = ['-is_superuser', 'username']  # added

    def get_short_name(self):
        """Return the short name for the user."""
        return self.given_names

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.surname_first:
            full_name = "%s %s" % (self.surname, self.given_names)
        else:
            full_name = "%s %s" % (self.given_names, self.surname)
        return full_name.strip()
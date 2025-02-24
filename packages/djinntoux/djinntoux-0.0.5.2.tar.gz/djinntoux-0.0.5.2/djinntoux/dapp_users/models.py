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

    timezone = TimeZoneField()

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
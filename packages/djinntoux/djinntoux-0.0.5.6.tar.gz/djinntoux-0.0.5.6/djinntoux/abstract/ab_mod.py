from django.conf import settings
from django.db import models
from tree_queries.models import TreeNode
from uuid6 import uuid7


class EditLink(models.Model):

    class Meta:
        abstract = True

    def get_edit_path(self):
        app = self._meta.app_label
        model = self._meta.model_name
        return f"/{settings.ADMIN_PATH}{app}/{model}/{self.pk}/change/"


class Timestamps(models.Model):
    db_row_created = models.DateTimeField(auto_now_add=True)
    db_row_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def compare_row_timestamps(self):
        created = self.db_row_created.replace(microsecond=0)
        updated = self.db_row_updated.replace(microsecond=0)
        if created == updated:
            return True
        else:
            return False


class UUIDpk7(models.Model):
    uuid_pk_v7 = models.UUIDField(primary_key=True, editable=False, default=uuid7)

    class Meta:
        abstract = True


class U7TimeEdit(UUIDpk7, Timestamps, EditLink):

    class Meta:
        abstract = True


class U7TimeEditTree(UUIDpk7, Timestamps, EditLink, TreeNode):

    class Meta:
        abstract = True
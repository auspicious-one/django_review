# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(max_length=255, blank=True, null=True)
    session_data = models.CharField(max_length=255, blank=True, null=True)
    expire_date = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_session'


class ReviewCount(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    starttime = models.IntegerField(blank=True, null=True)
    overtime = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_count'


class ReviewDeparment(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_deparment'


class ReviewScore(models.Model):
    uid = models.IntegerField(blank=True, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    did = models.IntegerField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)
    cid = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_score'


class ReviewUser(models.Model):
    name = models.CharField(max_length=10)
    deparment = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    bz = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'review_user'

# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

SEX = (
        (True, 'male'),
        (False, 'female')
    )


class Student(models.Model):

    name = models.CharField(max_length=30, null=True)
    sex = models.BooleanField(choices=SEX, default=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11, null=True)
    enabled = models.BooleanField(default=True)
    card_physicalID = models.CharField(max_length=50, null=True)
    cardUid = models.CharField(max_length=50, null=True)
    # cardHpt = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='students/photo', null=True, blank=True)

    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

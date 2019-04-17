# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-17 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('sex', models.BooleanField(choices=[(True, b'male'), (False, b'female')], default=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=11, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('card_physicalID', models.CharField(max_length=50, null=True)),
                ('cardUid', models.CharField(max_length=50, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=b'students/photo')),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

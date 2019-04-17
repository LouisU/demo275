# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-17 12:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=b'parent/photo')),
                ('sex', models.BooleanField(choices=[(True, b'male'), (False, b'female')], default=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=11, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='s_parent', to='students.Student')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='parent',
            unique_together=set([('id', 'student')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-01-19 15:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utenti', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='latitudine',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='longitudine',
        ),
    ]
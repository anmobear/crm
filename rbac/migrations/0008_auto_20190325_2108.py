# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-03-25 13:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_auto_20190325_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]

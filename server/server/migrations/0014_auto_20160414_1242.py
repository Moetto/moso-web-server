# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 12:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0013_auto_20160414_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='longitute',
            new_name='longitude',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20160321_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='userid',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]
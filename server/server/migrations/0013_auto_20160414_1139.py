# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 11:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_auto_20160413_1035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='latiture',
            new_name='latitute',
        ),
        migrations.AddField(
            model_name='location',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='server.Group'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-24 09:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0023_groupmember_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.Location'),
        ),
    ]

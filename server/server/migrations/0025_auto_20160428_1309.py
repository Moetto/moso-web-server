# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0024_task_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='estimated_completion_time',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]

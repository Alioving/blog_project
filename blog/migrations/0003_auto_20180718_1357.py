# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-18 05:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180716_1702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_time', 'title']},
        ),
    ]

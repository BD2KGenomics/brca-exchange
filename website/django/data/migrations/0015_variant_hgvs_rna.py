# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-07 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20161007_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='HGVS_RNA',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
    ]

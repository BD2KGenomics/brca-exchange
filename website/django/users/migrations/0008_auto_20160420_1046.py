# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-20 10:46


import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_myuser_key_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='myuser',
            name='password_token_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

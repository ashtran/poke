# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-29 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poke_app', '0002_auto_20171029_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poke',
            name='poker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pokes_id', to='poke_app.User'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-08 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABC', '0005_auto_20190508_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='bookImage',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]

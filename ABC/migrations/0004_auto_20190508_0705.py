# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-08 07:05
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ABC', '0003_auto_20190507_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='bookImage',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to=b''),
        ),
    ]

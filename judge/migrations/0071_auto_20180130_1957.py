# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-30 10:57
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0070_merge_20180127_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='access_code',
            field=models.CharField(blank=True, help_text='An optional code to prompt contestants before they are allowed to join the contest. Leave it blank to disable.', max_length=255, verbose_name='access code'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='key',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z0-9]+$', 'Contest id must be ^[a-z0-9]+$')], verbose_name='contest id'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='key',
            field=models.CharField(help_text='Organization name shows in URL', max_length=6, unique=True, validators=[django.core.validators.RegexValidator(b'^[A-Za-z0-9]+$', b'Identifier must contain letters and numbers only')], verbose_name='identifier'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='code',
            field=models.CharField(help_text='You can only use lower case and hyphen. e.g. pr0b1em-c0de', max_length=20, unique=True, validators=[django.core.validators.RegexValidator(b'^[a-zA-Z0-9\\-]+$', 'Problem code must be ^[a-z0-9]+$')], verbose_name='problem code'),
        ),
    ]

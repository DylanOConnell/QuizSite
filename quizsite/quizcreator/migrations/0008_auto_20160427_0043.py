# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizcreator', '0007_bugreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugreport',
            name='report',
            field=models.CharField(max_length=1000, verbose_name=b'Bug Report'),
        ),
    ]

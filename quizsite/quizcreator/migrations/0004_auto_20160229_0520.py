# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizcreator', '0003_answer_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='correct_type',
            field=models.CharField(default=b'FULL_W', max_length=6, choices=[(b'COR', b'Correct'), (b'PART_W', b'Partly Wrong'), (b'FULL_W', b'Fully Wrong')]),
        ),
    ]

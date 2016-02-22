# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizcreator', '0002_auto_20160217_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='answer_results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selected', models.BooleanField()),
                ('answer', models.ForeignKey(to='quizcreator.answer')),
                ('question', models.ForeignKey(to='quizcreator.questions')),
                ('quiz', models.ForeignKey(to='quizcreator.quiz')),
            ],
        ),
    ]

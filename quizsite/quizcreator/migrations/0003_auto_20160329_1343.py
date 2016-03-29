# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizcreator', '0002_auto_20160329_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selected', models.BooleanField()),
                ('answer', models.ForeignKey(to='quizcreator.Answer')),
                ('question', models.ForeignKey(to='quizcreator.Question')),
                ('quiz', models.ForeignKey(to='quizcreator.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(to='quizcreator.Quiz')),
                ('user', models.ForeignKey(to='quizcreator.User', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='answer_results',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='answer_results',
            name='question',
        ),
        migrations.RemoveField(
            model_name='answer_results',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quiz_results',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quiz_results',
            name='user',
        ),
        migrations.DeleteModel(
            name='Answer_results',
        ),
        migrations.DeleteModel(
            name='Quiz_results',
        ),
    ]

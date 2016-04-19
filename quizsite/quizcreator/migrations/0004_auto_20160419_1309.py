# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizcreator', '0003_auto_20160329_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selected', models.BooleanField()),
                ('answer', models.ForeignKey(to='quizcreator.Answer')),
                ('question', models.ForeignKey(to='quizcreator.Question')),
                ('quiz', models.ForeignKey(to='quizcreator.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(to='quizcreator.Quiz')),
            ],
        ),
        migrations.RemoveField(
            model_name='answerresults',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='answerresults',
            name='question',
        ),
        migrations.RemoveField(
            model_name='answerresults',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizresults',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='quizresults',
            name='user',
        ),
        migrations.DeleteModel(
            name='AnswerResults',
        ),
        migrations.DeleteModel(
            name='QuizResults',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='quizresult',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

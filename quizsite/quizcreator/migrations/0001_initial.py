# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('correct_type', models.CharField(default=b'FULL_W', max_length=6, choices=[(b'COR', b'Correct'), (b'PART_W', b'Partly Wrong'), (b'FULL_W', b'Fully Wrong')])),
            ],
        ),
        migrations.CreateModel(
            name='AnswerResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selected', models.BooleanField()),
                ('answer', models.ForeignKey(to='quizcreator.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report', models.CharField(max_length=1000, verbose_name=b'Bug Report')),
                ('timestamp', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOrdering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.PositiveIntegerField()),
                ('question', models.ForeignKey(to='quizcreator.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('questions', models.ManyToManyField(to='quizcreator.Question', through='quizcreator.QuestionOrdering')),
            ],
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('finished', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(to='quizcreator.Quiz')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='questionordering',
            name='quiz',
            field=models.ForeignKey(to='quizcreator.Quiz'),
        ),
        migrations.AddField(
            model_name='answerresult',
            name='question',
            field=models.ForeignKey(to='quizcreator.Question'),
        ),
        migrations.AddField(
            model_name='answerresult',
            name='quiz',
            field=models.ForeignKey(to='quizcreator.Quiz'),
        ),
        migrations.AddField(
            model_name='answerresult',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, to='quizcreator.Question', null=True),
        ),
    ]

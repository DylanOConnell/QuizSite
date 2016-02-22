# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizcreator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questions', models.ManyToManyField(to='quizcreator.questions')),
            ],
        ),
        migrations.CreateModel(
            name='quiz_results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('quiz', models.ForeignKey(to='quizcreator.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='questions_answers',
            name='answers',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer_text',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer_type',
        ),
        migrations.AddField(
            model_name='answer',
            name='correct_type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer',
            name='text',
            field=models.CharField(default='  ', max_length=200),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='questions_answers',
        ),
        migrations.AddField(
            model_name='quiz_results',
            name='user',
            field=models.ForeignKey(to='quizcreator.users'),
        ),
        migrations.AddField(
            model_name='questions',
            name='answers',
            field=models.ManyToManyField(to='quizcreator.answer'),
        ),
    ]
